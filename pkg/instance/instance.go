package instance

import (
	"context"
	"fmt"
	"io"
	"time"

	"github.com/pkg/errors"
	"github.com/sirupsen/logrus"
	"golang.org/x/sync/errgroup"
	grpccodes "google.golang.org/grpc/codes"
	grpcstatus "google.golang.org/grpc/status"
	"google.golang.org/protobuf/types/known/emptypb"

	spdkapi "github.com/longhorn/longhorn-spdk-engine/pkg/api"
	spdkclient "github.com/longhorn/longhorn-spdk-engine/pkg/client"

	"github.com/longhorn/longhorn-instance-manager/pkg/client"
	"github.com/longhorn/longhorn-instance-manager/pkg/meta"
	"github.com/longhorn/longhorn-instance-manager/pkg/types"

	rpc "github.com/longhorn/longhorn-instance-manager/pkg/imrpc"
)

const (
	maxMonitorRetryCount     = 10
	monitorRetryPollInterval = 1 * time.Second
)

type InstanceOps interface {
	InstanceCreate(*rpc.InstanceCreateRequest) (*rpc.InstanceResponse, error)
	InstanceDelete(*rpc.InstanceDeleteRequest) (*rpc.InstanceResponse, error)
	InstanceGet(*rpc.InstanceGetRequest) (*rpc.InstanceResponse, error)
	InstanceList(map[string]*rpc.InstanceResponse) error
	InstanceReplace(*rpc.InstanceReplaceRequest) (*rpc.InstanceResponse, error)
	InstanceLog(*rpc.InstanceLogRequest, rpc.InstanceService_InstanceLogServer) error
}

type V1DataEngineInstanceOps struct {
	processManagerServiceAddress string
}
type V2DataEngineInstanceOps struct {
	spdkServiceAddress string
}

type Server struct {
	ctx           context.Context
	logsDir       string
	HealthChecker HealthChecker

	v2DataEngineEnabled bool
	ops                 map[rpc.DataEngine]InstanceOps
}

func NewServer(ctx context.Context, logsDir, processManagerServiceAddress, spdkServiceAddress string, v2DataEngineEnabled bool) (*Server, error) {
	ops := map[rpc.DataEngine]InstanceOps{
		rpc.DataEngine_DATA_ENGINE_V1: V1DataEngineInstanceOps{
			processManagerServiceAddress: processManagerServiceAddress,
		},
		rpc.DataEngine_DATA_ENGINE_V2: V2DataEngineInstanceOps{
			spdkServiceAddress: spdkServiceAddress,
		},
	}

	s := &Server{
		ctx:                 ctx,
		logsDir:             logsDir,
		v2DataEngineEnabled: v2DataEngineEnabled,
		HealthChecker:       &GRPCHealthChecker{},
		ops:                 ops,
	}

	go s.startMonitoring()

	return s, nil
}

func (s *Server) startMonitoring() {
	done := false
	for {
		select {
		case <-s.ctx.Done():
			logrus.Infof("%s: stopped monitoring replicas due to the context done", types.InstanceGrpcService)
			done = true
		}
		if done {
			break
		}
	}
}

func (s *Server) VersionGet(ctx context.Context, req *emptypb.Empty) (*rpc.VersionResponse, error) {
	v := meta.GetVersion()
	return &rpc.VersionResponse{
		Version:   v.Version,
		GitCommit: v.GitCommit,
		BuildDate: v.BuildDate,

		InstanceManagerAPIVersion:    int64(v.InstanceManagerAPIVersion),
		InstanceManagerAPIMinVersion: int64(v.InstanceManagerAPIMinVersion),

		InstanceManagerProxyAPIVersion:    int64(v.InstanceManagerProxyAPIVersion),
		InstanceManagerProxyAPIMinVersion: int64(v.InstanceManagerProxyAPIMinVersion),
	}, nil
}

func (s *Server) InstanceCreate(ctx context.Context, req *rpc.InstanceCreateRequest) (*rpc.InstanceResponse, error) {
	logrus.WithFields(logrus.Fields{
		"name":       req.Spec.Name,
		"type":       req.Spec.Type,
		"dataEngine": req.Spec.DataEngine,
	}).Info("Creating instance")

	ops, ok := s.ops[req.Spec.DataEngine]
	if !ok {
		return nil, grpcstatus.Errorf(grpccodes.Unimplemented, "unsupported data engine %v", req.Spec.DataEngine)
	}
	return ops.InstanceCreate(req)
}

func (ops V1DataEngineInstanceOps) InstanceCreate(req *rpc.InstanceCreateRequest) (*rpc.InstanceResponse, error) {
	if req.Spec.ProcessInstanceSpec == nil {
		return nil, grpcstatus.Error(grpccodes.InvalidArgument, "ProcessInstanceSpec is required for longhorn data engine")
	}

	pmClient, err := client.NewProcessManagerClient("tcp://"+ops.processManagerServiceAddress, nil)
	if err != nil {
		return nil, grpcstatus.Error(grpccodes.Internal, errors.Wrapf(err, "failed to create ProcessManagerClient").Error())
	}
	defer pmClient.Close()

	process, err := pmClient.ProcessCreate(req.Spec.Name, req.Spec.ProcessInstanceSpec.Binary, int(req.Spec.PortCount), req.Spec.ProcessInstanceSpec.Args, req.Spec.PortArgs)
	if err != nil {
		return nil, err
	}
	return processResponseToInstanceResponse(process), nil
}

func (ops V2DataEngineInstanceOps) InstanceCreate(req *rpc.InstanceCreateRequest) (*rpc.InstanceResponse, error) {
	c, err := spdkclient.NewSPDKClient(ops.spdkServiceAddress)
	if err != nil {
		return nil, grpcstatus.Error(grpccodes.Internal, errors.Wrapf(err, "failed to create SPDK client").Error())
	}
	defer c.Close()

	switch req.Spec.Type {
	case types.InstanceTypeEngine:
		engine, err := c.EngineCreate(req.Spec.Name, req.Spec.VolumeName, req.Spec.SpdkInstanceSpec.Frontend, req.Spec.SpdkInstanceSpec.Size, req.Spec.SpdkInstanceSpec.ReplicaAddressMap, req.Spec.PortCount)
		if err != nil {
			return nil, err
		}
		return engineResponseToInstanceResponse(engine), nil
	case types.InstanceTypeReplica:
		replica, err := c.ReplicaCreate(req.Spec.Name, req.Spec.SpdkInstanceSpec.DiskName, req.Spec.SpdkInstanceSpec.DiskUuid, req.Spec.SpdkInstanceSpec.Size, req.Spec.SpdkInstanceSpec.ExposeRequired, req.Spec.PortCount)
		if err != nil {
			return nil, err
		}
		return replicaResponseToInstanceResponse(replica), nil
	default:
		return nil, grpcstatus.Errorf(grpccodes.InvalidArgument, "unknown instance type %v", req.Spec.Type)
	}
}

func (s *Server) InstanceDelete(ctx context.Context, req *rpc.InstanceDeleteRequest) (*rpc.InstanceResponse, error) {
	logrus.WithFields(logrus.Fields{
		"name":            req.Name,
		"type":            req.Type,
		"dataEngine":      req.DataEngine,
		"diskUuid":        req.DiskUuid,
		"cleanupRequired": req.CleanupRequired,
	}).Info("Deleting instance")

	ops, ok := s.ops[req.DataEngine]
	if !ok {
		return nil, grpcstatus.Errorf(grpccodes.Unimplemented, "unsupported data engine %v", req.DataEngine)
	}
	return ops.InstanceDelete(req)
}

func (ops V1DataEngineInstanceOps) InstanceDelete(req *rpc.InstanceDeleteRequest) (*rpc.InstanceResponse, error) {
	pmClient, err := client.NewProcessManagerClient("tcp://"+ops.processManagerServiceAddress, nil)
	if err != nil {
		return nil, grpcstatus.Error(grpccodes.Internal, errors.Wrapf(err, "failed to create ProcessManagerClient").Error())
	}
	defer pmClient.Close()

	process, err := pmClient.ProcessDelete(req.Name)
	if err != nil {
		return nil, err
	}
	return processResponseToInstanceResponse(process), nil
}

func (ops V2DataEngineInstanceOps) InstanceDelete(req *rpc.InstanceDeleteRequest) (*rpc.InstanceResponse, error) {
	c, err := spdkclient.NewSPDKClient(ops.spdkServiceAddress)
	if err != nil {
		return nil, grpcstatus.Error(grpccodes.Internal, errors.Wrapf(err, "failed to create SPDK client").Error())
	}
	defer c.Close()

	switch req.Type {
	case types.InstanceTypeEngine:
		if req.CleanupRequired {
			err = c.EngineDelete(req.Name)
		}
	case types.InstanceTypeReplica:
		err = c.ReplicaDelete(req.Name, req.CleanupRequired)
	default:
		err = grpcstatus.Errorf(grpccodes.InvalidArgument, "unknown instance type %v", req.Type)
	}
	if err != nil {
		return nil, err
	}

	return &rpc.InstanceResponse{
		Spec: &rpc.InstanceSpec{
			Name: req.Name,
		},
		Status: &rpc.InstanceStatus{
			State: types.ProcessStateStopped,
		},
		Deleted: true,
	}, nil
}

func (s *Server) InstanceGet(ctx context.Context, req *rpc.InstanceGetRequest) (*rpc.InstanceResponse, error) {
	logrus.WithFields(logrus.Fields{
		"name":       req.Name,
		"type":       req.Type,
		"dataEngine": req.DataEngine,
	}).Trace("Getting instance")

	ops, ok := s.ops[req.DataEngine]
	if !ok {
		return nil, grpcstatus.Errorf(grpccodes.Unimplemented, "unsupported data engine %v", req.DataEngine)
	}
	return ops.InstanceGet(req)
}

func (ops V1DataEngineInstanceOps) InstanceGet(req *rpc.InstanceGetRequest) (*rpc.InstanceResponse, error) {
	pmClient, err := client.NewProcessManagerClient("tcp://"+ops.processManagerServiceAddress, nil)
	if err != nil {
		return nil, grpcstatus.Error(grpccodes.Internal, errors.Wrapf(err, "failed to create ProcessManagerClient").Error())
	}
	defer pmClient.Close()

	process, err := pmClient.ProcessGet(req.Name)
	if err != nil {
		return nil, err
	}
	return processResponseToInstanceResponse(process), nil
}

func (ops V2DataEngineInstanceOps) InstanceGet(req *rpc.InstanceGetRequest) (*rpc.InstanceResponse, error) {
	c, err := spdkclient.NewSPDKClient(ops.spdkServiceAddress)
	if err != nil {
		return nil, grpcstatus.Error(grpccodes.Internal, errors.Wrapf(err, "failed to create SPDK client").Error())
	}
	defer c.Close()

	switch req.Type {
	case types.InstanceTypeEngine:
		engine, err := c.EngineGet(req.Name)
		if err != nil {
			return nil, err
		}
		return engineResponseToInstanceResponse(engine), nil
	case types.InstanceTypeReplica:
		replica, err := c.ReplicaGet(req.Name)
		if err != nil {
			return nil, err
		}
		return replicaResponseToInstanceResponse(replica), nil
	default:
		return nil, grpcstatus.Errorf(grpccodes.InvalidArgument, "unknown instance type %v", req.Type)
	}
}

func (s *Server) InstanceList(ctx context.Context, req *emptypb.Empty) (*rpc.InstanceListResponse, error) {
	logrus.WithFields(logrus.Fields{}).Trace("Listing instances")

	instances := map[string]*rpc.InstanceResponse{}

	err := s.ops[rpc.DataEngine_DATA_ENGINE_V1].InstanceList(instances)
	if err != nil {
		return nil, err
	}

	if s.v2DataEngineEnabled {
		err := s.ops[rpc.DataEngine_DATA_ENGINE_V2].InstanceList(instances)
		if err != nil {
			return nil, err
		}
	}

	return &rpc.InstanceListResponse{
		Instances: instances,
	}, nil
}

func (ops V1DataEngineInstanceOps) InstanceList(instances map[string]*rpc.InstanceResponse) error {
	pmClient, err := client.NewProcessManagerClient("tcp://"+ops.processManagerServiceAddress, nil)
	if err != nil {
		return grpcstatus.Error(grpccodes.Internal, errors.Wrapf(err, "failed to create ProcessManagerClient").Error())
	}
	defer pmClient.Close()

	processes, err := pmClient.ProcessList()
	if err != nil {
		return err
	}
	for _, process := range processes {
		instances[process.Spec.Name] = processResponseToInstanceResponse(process)
	}
	return nil
}

func (ops V2DataEngineInstanceOps) InstanceList(instances map[string]*rpc.InstanceResponse) error {
	c, err := spdkclient.NewSPDKClient(ops.spdkServiceAddress)
	if err != nil {
		return grpcstatus.Error(grpccodes.Internal, errors.Wrapf(err, "failed to create SPDK client").Error())
	}
	defer c.Close()

	replicas, err := c.ReplicaList()
	if err != nil {
		return err
	}
	for _, replica := range replicas {
		instances[replica.Name] = replicaResponseToInstanceResponse(replica)
	}

	engines, err := c.EngineList()
	if err != nil {
		return err
	}
	for _, engine := range engines {
		instances[engine.Name] = engineResponseToInstanceResponse(engine)
	}
	return nil
}

func (s *Server) InstanceReplace(ctx context.Context, req *rpc.InstanceReplaceRequest) (*rpc.InstanceResponse, error) {
	logrus.WithFields(logrus.Fields{
		"name":       req.Spec.Name,
		"type":       req.Spec.Type,
		"dataEngine": req.Spec.DataEngine,
	}).Info("Replacing instance")

	ops, ok := s.ops[req.Spec.DataEngine]
	if !ok {
		return nil, grpcstatus.Errorf(grpccodes.Unimplemented, "unsupported data engine %v", req.Spec.DataEngine)
	}
	return ops.InstanceReplace(req)
}

func (ops V1DataEngineInstanceOps) InstanceReplace(req *rpc.InstanceReplaceRequest) (*rpc.InstanceResponse, error) {
	if req.Spec.ProcessInstanceSpec == nil {
		return nil, grpcstatus.Error(grpccodes.InvalidArgument, "ProcessInstanceSpec is required for longhorn data engine")
	}

	pmClient, err := client.NewProcessManagerClient("tcp://"+ops.processManagerServiceAddress, nil)
	if err != nil {
		return nil, grpcstatus.Error(grpccodes.Internal, errors.Wrapf(err, "failed to create ProcessManagerClient").Error())
	}
	defer pmClient.Close()

	process, err := pmClient.ProcessReplace(req.Spec.Name,
		req.Spec.ProcessInstanceSpec.Binary, int(req.Spec.PortCount), req.Spec.ProcessInstanceSpec.Args, req.Spec.PortArgs, req.TerminateSignal)
	if err != nil {
		return nil, err
	}

	return processResponseToInstanceResponse(process), nil
}

func (ops V2DataEngineInstanceOps) InstanceReplace(req *rpc.InstanceReplaceRequest) (*rpc.InstanceResponse, error) {
	return nil, grpcstatus.Error(grpccodes.Unimplemented, "v2 data engine instance replace is not supported")
}

func (s *Server) InstanceLog(req *rpc.InstanceLogRequest, srv rpc.InstanceService_InstanceLogServer) error {
	logrus.WithFields(logrus.Fields{
		"name":       req.Name,
		"type":       req.Type,
		"dataEngine": req.DataEngine,
	}).Info("Getting instance log")

	ops, ok := s.ops[req.DataEngine]
	if !ok {
		return grpcstatus.Errorf(grpccodes.Unimplemented, "unsupported data engine %v", req.DataEngine)
	}
	return ops.InstanceLog(req, srv)
}

func (ops V1DataEngineInstanceOps) InstanceLog(req *rpc.InstanceLogRequest, srv rpc.InstanceService_InstanceLogServer) error {
	pmClient, err := client.NewProcessManagerClient("tcp://"+ops.processManagerServiceAddress, nil)
	if err != nil {
		return grpcstatus.Error(grpccodes.Internal, errors.Wrapf(err, "failed to create ProcessManagerClient").Error())
	}
	defer pmClient.Close()

	stream, err := pmClient.ProcessLog(context.Background(), req.Name)
	if err != nil {
		return err
	}
	for {
		line, err := stream.Recv()
		if err == io.EOF {
			break
		} else if err != nil {
			logrus.WithError(err).Error("Failed to receive log")
			return err
		}

		if err := srv.Send(&rpc.LogResponse{Line: line}); err != nil {
			return err
		}
	}
	return nil
}

func (ops V2DataEngineInstanceOps) InstanceLog(req *rpc.InstanceLogRequest, srv rpc.InstanceService_InstanceLogServer) error {
	return grpcstatus.Error(grpccodes.Unimplemented, "v2 data engine instance log is not supported")
}

func (s *Server) handleNotify(ctx context.Context, notifyChan chan struct{}, srv rpc.InstanceService_InstanceWatchServer) error {
	logrus.Info("Start handling notify")

	for {
		select {
		case <-ctx.Done():
			logrus.Info("Stopped handling notify due to the context done")
			return ctx.Err()
		case <-notifyChan:
			if err := srv.Send(&emptypb.Empty{}); err != nil {
				return errors.Wrap(err, "failed to send instance response")
			}
		}
	}
}

func (s *Server) InstanceWatch(req *emptypb.Empty, srv rpc.InstanceService_InstanceWatchServer) error {
	logrus.Info("Start watching instances")

	done := make(chan struct{})

	clients := map[string]interface{}{}
	go func() {
		<-done

		logrus.Info("Stopped clients for watching instances")
		for name, c := range clients {
			switch c := c.(type) {
			case *client.ProcessManagerClient:
				c.Close()
			case *spdkclient.SPDKClient:
				c.Close()
			}
			delete(clients, name)
		}
		close(done)
	}()

	// Create a client for watching processes
	ops := s.ops[rpc.DataEngine_DATA_ENGINE_V1].(V1DataEngineInstanceOps)
	pmClient, err := client.NewProcessManagerClient("tcp://"+ops.processManagerServiceAddress, nil)
	if err != nil {
		done <- struct{}{}
		return grpcstatus.Error(grpccodes.Internal, errors.Wrapf(err, "failed to create ProcessManagerClient").Error())
	}
	clients["processManagerClient"] = pmClient

	var spdkClient *spdkclient.SPDKClient
	if s.v2DataEngineEnabled {
		// Create a client for watching SPDK engines and replicas
		ops := s.ops[rpc.DataEngine_DATA_ENGINE_V2].(V2DataEngineInstanceOps)
		spdkClient, err = spdkclient.NewSPDKClient(ops.spdkServiceAddress)
		if err != nil {
			done <- struct{}{}
			return grpcstatus.Error(grpccodes.Internal, errors.Wrapf(err, "failed to create SPDK client").Error())
		}
		clients["spdkClient"] = spdkClient
	}

	notifyChan := make(chan struct{}, 1024)
	defer close(notifyChan)

	g, ctx := errgroup.WithContext(s.ctx)

	g.Go(func() error {
		defer func() {
			// Close the clients for closing streams and unblocking notifier Recv() with error.
			done <- struct{}{}
		}()
		return s.handleNotify(ctx, notifyChan, srv)
	})

	g.Go(func() error {
		return s.watchProcess(ctx, req, pmClient, notifyChan)
	})

	if s.v2DataEngineEnabled {
		g.Go(func() error {
			return s.watchSPDKEngine(ctx, req, spdkClient, notifyChan)
		})

		g.Go(func() error {
			return s.watchSPDKReplica(ctx, req, spdkClient, notifyChan)
		})
	}

	if err := g.Wait(); err != nil {
		logrus.WithError(err).Error("Failed to watch instances")
		return errors.Wrap(err, "failed to watch instances")
	}

	return nil
}

func (s *Server) watchSPDKReplica(ctx context.Context, req *emptypb.Empty, client *spdkclient.SPDKClient, notifyChan chan struct{}) error {
	logrus.Info("Start watching SPDK replicas")

	notifier, err := client.ReplicaWatch(context.Background())
	if err != nil {
		return errors.Wrap(err, "failed to create SPDK replica watch notifier")
	}

	failureCount := 0
	for {
		if failureCount >= maxMonitorRetryCount {
			logrus.Errorf("Continuously receiving errors for %v times, stopping watching SPDK replicas", maxMonitorRetryCount)
			return fmt.Errorf("continuously receiving errors for %v times, stopping watching SPDK replicas", maxMonitorRetryCount)
		}

		select {
		case <-ctx.Done():
			logrus.Info("Stopped watching SPDK replicas")
			return ctx.Err()
		default:
			_, err := notifier.Recv()
			if err != nil {
				status, ok := grpcstatus.FromError(err)
				if ok && status.Code() == grpccodes.Canceled {
					logrus.WithError(err).Warn("SPDK replica watch is canceled")
					return err
				}
				logrus.WithError(err).Error("Failed to receive next item in SPDK replica watch")
				time.Sleep(monitorRetryPollInterval)
				failureCount++
			} else {
				notifyChan <- struct{}{}
			}
		}
	}
}

func (s *Server) watchSPDKEngine(ctx context.Context, req *emptypb.Empty, client *spdkclient.SPDKClient, notifyChan chan struct{}) error {
	logrus.Info("Start watching SPDK engines")

	notifier, err := client.EngineWatch(context.Background())
	if err != nil {
		return errors.Wrap(err, "failed to create SPDK engine watch notifier")
	}

	failureCount := 0
	for {
		if failureCount >= maxMonitorRetryCount {
			logrus.Errorf("Continuously receiving errors for %v times, stopping watching SPDK engines", maxMonitorRetryCount)
			return fmt.Errorf("continuously receiving errors for %v times, stopping watching SPDK engines", maxMonitorRetryCount)
		}

		select {
		case <-ctx.Done():
			logrus.Info("Stopped watching SPDK engines")
			return ctx.Err()
		default:
			_, err := notifier.Recv()
			if err != nil {
				status, ok := grpcstatus.FromError(err)
				if ok && status.Code() == grpccodes.Canceled {
					logrus.WithError(err).Warn("SPDK engine watch is canceled")
					return err
				}
				logrus.WithError(err).Error("Failed to receive next item in SPDK engine watch")
				time.Sleep(monitorRetryPollInterval)
				failureCount++
			} else {
				notifyChan <- struct{}{}
			}
		}
	}
}

func (s *Server) watchProcess(ctx context.Context, req *emptypb.Empty, client *client.ProcessManagerClient, notifyChan chan struct{}) error {
	logrus.Info("Start watching processes")

	notifier, err := client.ProcessWatch(context.Background())
	if err != nil {
		return errors.Wrap(err, "failed to create process watch notifier")
	}

	failureCount := 0
	for {
		if failureCount >= maxMonitorRetryCount {
			logrus.Errorf("Continuously receiving errors for %v times, stopping watching processes", maxMonitorRetryCount)
			return fmt.Errorf("continuously receiving errors for %v times, stopping watching processes", maxMonitorRetryCount)
		}

		select {
		case <-ctx.Done():
			logrus.Info("Stopped watching processes")
			return ctx.Err()
		default:
			_, err := notifier.Recv()
			if err != nil {
				status, ok := grpcstatus.FromError(err)
				if ok && status.Code() == grpccodes.Canceled {
					logrus.WithError(err).Warn("Process watch is canceled")
					return err
				}
				logrus.WithError(err).Error("Failed to receive next item in process watch")
				time.Sleep(monitorRetryPollInterval)
				failureCount++
			} else {
				notifyChan <- struct{}{}
			}
		}
	}
}

func processResponseToInstanceResponse(p *rpc.ProcessResponse) *rpc.InstanceResponse {
	return &rpc.InstanceResponse{
		Spec: &rpc.InstanceSpec{
			Name: p.Spec.Name,
			// Leave Type empty. It will be determined in longhorn manager.
			Type: "",
			// Deprecated
			BackendStoreDriver: rpc.BackendStoreDriver_v1,
			DataEngine:         rpc.DataEngine_DATA_ENGINE_V1,
			ProcessInstanceSpec: &rpc.ProcessInstanceSpec{
				Binary: p.Spec.Binary,
				Args:   p.Spec.Args,
			},
			PortCount: int32(p.Spec.PortCount),
			PortArgs:  p.Spec.PortArgs,
		},
		Status: &rpc.InstanceStatus{
			State:      p.Status.State,
			PortStart:  p.Status.PortStart,
			PortEnd:    p.Status.PortEnd,
			ErrorMsg:   p.Status.ErrorMsg,
			Conditions: p.Status.Conditions,
		},
		Deleted: p.Deleted,
	}
}

func replicaResponseToInstanceResponse(r *spdkapi.Replica) *rpc.InstanceResponse {
	return &rpc.InstanceResponse{
		Spec: &rpc.InstanceSpec{
			Name: r.Name,
			Type: types.InstanceTypeReplica,
			// Deprecated
			BackendStoreDriver: rpc.BackendStoreDriver_v2,
			DataEngine:         rpc.DataEngine_DATA_ENGINE_V2,
		},
		Status: &rpc.InstanceStatus{
			State:      r.State,
			ErrorMsg:   r.ErrorMsg,
			PortStart:  r.PortStart,
			PortEnd:    r.PortEnd,
			Conditions: make(map[string]bool),
		},
	}
}

func engineResponseToInstanceResponse(e *spdkapi.Engine) *rpc.InstanceResponse {
	return &rpc.InstanceResponse{
		Spec: &rpc.InstanceSpec{
			Name: e.Name,
			Type: types.InstanceTypeEngine,
			// Deprecated
			BackendStoreDriver: rpc.BackendStoreDriver_v2,
			DataEngine:         rpc.DataEngine_DATA_ENGINE_V2,
		},
		Status: &rpc.InstanceStatus{
			State:      e.State,
			ErrorMsg:   e.ErrorMsg,
			PortStart:  e.Port,
			PortEnd:    e.Port,
			Conditions: make(map[string]bool),
		},
	}
}
