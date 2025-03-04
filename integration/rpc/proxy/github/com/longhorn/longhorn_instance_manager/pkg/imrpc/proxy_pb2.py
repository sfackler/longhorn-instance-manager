# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: github.com/longhorn/longhorn-instance-manager/pkg/imrpc/proxy.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from github.com.longhorn.longhorn_engine.proto.ptypes import controller_pb2 as github_dot_com_dot_longhorn_dot_longhorn__engine_dot_proto_dot_ptypes_dot_controller__pb2
from github.com.longhorn.longhorn_engine.proto.ptypes import syncagent_pb2 as github_dot_com_dot_longhorn_dot_longhorn__engine_dot_proto_dot_ptypes_dot_syncagent__pb2
from github.com.longhorn.longhorn_instance_manager.pkg.imrpc import common_pb2 as github_dot_com_dot_longhorn_dot_longhorn__instance__manager_dot_pkg_dot_imrpc_dot_common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nCgithub.com/longhorn/longhorn-instance-manager/pkg/imrpc/proxy.proto\x12\x05imrpc\x1a\x1bgoogle/protobuf/empty.proto\x1a\x41github.com/longhorn/longhorn-engine/proto/ptypes/controller.proto\x1a@github.com/longhorn/longhorn-engine/proto/ptypes/syncagent.proto\x1a\x44github.com/longhorn/longhorn-instance-manager/pkg/imrpc/common.proto\"\xb4\x01\n\x12ProxyEngineRequest\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12;\n\x14\x62\x61\x63kend_store_driver\x18\x02 \x01(\x0e\x32\x19.imrpc.BackendStoreDriverB\x02\x18\x01\x12\x13\n\x0b\x65ngine_name\x18\x03 \x01(\t\x12\x13\n\x0bvolume_name\x18\x04 \x01(\t\x12&\n\x0b\x64\x61ta_engine\x18\x05 \x01(\x0e\x32\x11.imrpc.DataEngine\"D\n\x1a\x45ngineVersionProxyResponse\x12&\n\x07version\x18\x01 \x01(\x0b\x32\x15.ptypes.VersionOutput\">\n\x1c\x45ngineVolumeGetProxyResponse\x12\x1e\n\x06volume\x18\x01 \x01(\x0b\x32\x0e.ptypes.Volume\"\x81\x01\n\x19\x45ngineVolumeExpandRequest\x12\x37\n\x14proxy_engine_request\x18\x01 \x01(\x0b\x32\x19.imrpc.ProxyEngineRequest\x12+\n\x06\x65xpand\x18\x02 \x01(\x0b\x32\x1b.ptypes.VolumeExpandRequest\"\x97\x01\n EngineVolumeFrontendStartRequest\x12\x37\n\x14proxy_engine_request\x18\x01 \x01(\x0b\x32\x19.imrpc.ProxyEngineRequest\x12:\n\x0e\x66rontend_start\x18\x02 \x01(\x0b\x32\".ptypes.VolumeFrontendStartRequest\"\x8e\x01\n\x1b\x45ngineVolumeSnapshotRequest\x12\x37\n\x14proxy_engine_request\x18\x01 \x01(\x0b\x32\x19.imrpc.ProxyEngineRequest\x12\x36\n\x0fsnapshot_volume\x18\x02 \x01(\x0b\x32\x1d.ptypes.VolumeSnapshotRequest\"R\n!EngineVolumeSnapshotProxyResponse\x12-\n\x08snapshot\x18\x01 \x01(\x0b\x32\x1b.ptypes.VolumeSnapshotReply\"\xb6\x01\n/EngineVolumeUnmapMarkSnapChainRemovedSetRequest\x12\x37\n\x14proxy_engine_request\x18\x01 \x01(\x0b\x32\x19.imrpc.ProxyEngineRequest\x12J\n\x0funmap_mark_snap\x18\x02 \x01(\x0b\x32\x31.ptypes.VolumeUnmapMarkSnapChainRemovedSetRequest\"\x9a\x01\n&EngineVolumeSnapshotMaxCountSetRequest\x12\x37\n\x14proxy_engine_request\x18\x01 \x01(\x0b\x32\x19.imrpc.ProxyEngineRequest\x12\x37\n\x05\x63ount\x18\x02 \x01(\x0b\x32(.ptypes.VolumeSnapshotMaxCountSetRequest\"\x97\x01\n%EngineVolumeSnapshotMaxSizeSetRequest\x12\x37\n\x14proxy_engine_request\x18\x01 \x01(\x0b\x32\x19.imrpc.ProxyEngineRequest\x12\x35\n\x04size\x18\x02 \x01(\x0b\x32\'.ptypes.VolumeSnapshotMaxSizeSetRequest\"\xb0\x01\n\x1f\x45ngineSnapshotListProxyResponse\x12@\n\x05\x64isks\x18\x01 \x03(\x0b\x32\x31.imrpc.EngineSnapshotListProxyResponse.DisksEntry\x1aK\n\nDisksEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12,\n\x05value\x18\x02 \x01(\x0b\x32\x1d.imrpc.EngineSnapshotDiskInfo:\x02\x38\x01\"\xd6\x02\n\x16\x45ngineSnapshotDiskInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06parent\x18\x02 \x01(\t\x12=\n\x08\x63hildren\x18\x03 \x03(\x0b\x32+.imrpc.EngineSnapshotDiskInfo.ChildrenEntry\x12\x0f\n\x07removed\x18\x04 \x01(\x08\x12\x14\n\x0cuser_created\x18\x05 \x01(\x08\x12\x0f\n\x07\x63reated\x18\x06 \x01(\t\x12\x0c\n\x04size\x18\x07 \x01(\t\x12\x39\n\x06labels\x18\x08 \x03(\x0b\x32).imrpc.EngineSnapshotDiskInfo.LabelsEntry\x1a/\n\rChildrenEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x08:\x02\x38\x01\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"d\n\x1b\x45ngineSnapshotRevertRequest\x12\x37\n\x14proxy_engine_request\x18\x01 \x01(\x0b\x32\x19.imrpc.ProxyEngineRequest\x12\x0c\n\x04name\x18\x02 \x01(\t\"r\n\x1a\x45ngineSnapshotPurgeRequest\x12\x37\n\x14proxy_engine_request\x18\x01 \x01(\x0b\x32\x19.imrpc.ProxyEngineRequest\x12\x1b\n\x13skip_if_in_progress\x18\x02 \x01(\x08\"\xc7\x01\n&EngineSnapshotPurgeStatusProxyResponse\x12I\n\x06status\x18\x01 \x03(\x0b\x32\x39.imrpc.EngineSnapshotPurgeStatusProxyResponse.StatusEntry\x1aR\n\x0bStatusEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x32\n\x05value\x18\x02 \x01(\x0b\x32#.ptypes.SnapshotPurgeStatusResponse:\x02\x38\x01\"\x8b\x02\n\x1a\x45ngineSnapshotCloneRequest\x12\x37\n\x14proxy_engine_request\x18\x01 \x01(\x0b\x32\x19.imrpc.ProxyEngineRequest\x12\x1b\n\x13\x66rom_engine_address\x18\x02 \x01(\t\x12\x15\n\rsnapshot_name\x18\x03 \x01(\t\x12%\n\x1d\x65xport_backing_image_if_exist\x18\x04 \x01(\x08\x12%\n\x1d\x66ile_sync_http_client_timeout\x18\x05 \x01(\x05\x12\x18\n\x10\x66rom_engine_name\x18\x06 \x01(\t\x12\x18\n\x10\x66rom_volume_name\x18\x07 \x01(\t\"\xc7\x01\n&EngineSnapshotCloneStatusProxyResponse\x12I\n\x06status\x18\x01 \x03(\x0b\x32\x39.imrpc.EngineSnapshotCloneStatusProxyResponse.StatusEntry\x1aR\n\x0bStatusEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x32\n\x05value\x18\x02 \x01(\x0b\x32#.ptypes.SnapshotCloneStatusResponse:\x02\x38\x01\"e\n\x1b\x45ngineSnapshotRemoveRequest\x12\x37\n\x14proxy_engine_request\x18\x01 \x01(\x0b\x32\x19.imrpc.ProxyEngineRequest\x12\r\n\x05names\x18\x02 \x03(\t\"\xa4\x03\n\x1b\x45ngineSnapshotBackupRequest\x12\x37\n\x14proxy_engine_request\x18\x01 \x01(\x0b\x32\x19.imrpc.ProxyEngineRequest\x12\x0c\n\x04\x65nvs\x18\x08 \x03(\t\x12\x13\n\x0b\x62\x61\x63kup_name\x18\x02 \x01(\t\x12\x15\n\rsnapshot_name\x18\x03 \x01(\t\x12\x15\n\rbackup_target\x18\x04 \x01(\t\x12\x1a\n\x12\x62\x61\x63king_image_name\x18\x05 \x01(\t\x12\x1e\n\x16\x62\x61\x63king_image_checksum\x18\x06 \x01(\t\x12>\n\x06labels\x18\x07 \x03(\x0b\x32..imrpc.EngineSnapshotBackupRequest.LabelsEntry\x12\x1a\n\x12\x63ompression_method\x18\t \x01(\t\x12\x18\n\x10\x63oncurrent_limit\x18\n \x01(\x05\x12\x1a\n\x12storage_class_name\x18\x0b \x01(\t\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"_\n!EngineSnapshotBackupProxyResponse\x12\x11\n\tbackup_id\x18\x01 \x01(\t\x12\x0f\n\x07replica\x18\x02 \x01(\t\x12\x16\n\x0eis_incremental\x18\x03 \x01(\x08\"\xa0\x01\n!EngineSnapshotBackupStatusRequest\x12\x37\n\x14proxy_engine_request\x18\x01 \x01(\x0b\x32\x19.imrpc.ProxyEngineRequest\x12\x13\n\x0b\x62\x61\x63kup_name\x18\x02 \x01(\t\x12\x17\n\x0freplica_address\x18\x03 \x01(\t\x12\x14\n\x0creplica_name\x18\x04 \x01(\t\"\x9d\x01\n\'EngineSnapshotBackupStatusProxyResponse\x12\x12\n\nbackup_url\x18\x01 \x01(\t\x12\r\n\x05\x65rror\x18\x02 \x01(\t\x12\x10\n\x08progress\x18\x03 \x01(\x05\x12\x15\n\rsnapshot_name\x18\x04 \x01(\t\x12\r\n\x05state\x18\x05 \x01(\t\x12\x17\n\x0freplica_address\x18\x06 \x01(\t\"\xaf\x01\n\x1a\x45ngineBackupRestoreRequest\x12\x37\n\x14proxy_engine_request\x18\x01 \x01(\x0b\x32\x19.imrpc.ProxyEngineRequest\x12\x0c\n\x04\x65nvs\x18\x02 \x03(\t\x12\x0b\n\x03url\x18\x03 \x01(\t\x12\x0e\n\x06target\x18\x04 \x01(\t\x12\x13\n\x0bvolume_name\x18\x05 \x01(\t\x12\x18\n\x10\x63oncurrent_limit\x18\x06 \x01(\x05\"5\n EngineBackupRestoreProxyResponse\x12\x11\n\ttaskError\x18\x01 \x01(\x0c\"\xc4\x01\n&EngineBackupRestoreStatusProxyResponse\x12I\n\x06status\x18\x01 \x03(\x0b\x32\x39.imrpc.EngineBackupRestoreStatusProxyResponse.StatusEntry\x1aO\n\x0bStatusEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12/\n\x05value\x18\x02 \x01(\x0b\x32 .imrpc.EngineBackupRestoreStatus:\x02\x38\x01\"\xc0\x01\n\x19\x45ngineBackupRestoreStatus\x12\x14\n\x0cis_restoring\x18\x01 \x01(\x08\x12\x15\n\rlast_restored\x18\x02 \x01(\t\x12 \n\x18\x63urrent_restoring_backup\x18\x03 \x01(\t\x12\x10\n\x08progress\x18\x04 \x01(\x05\x12\r\n\x05\x65rror\x18\x05 \x01(\t\x12\x10\n\x08\x66ilename\x18\x06 \x01(\t\x12\r\n\x05state\x18\x07 \x01(\t\x12\x12\n\nbackup_url\x18\x08 \x01(\t\"[\n EngineBackupRestoreFinishRequest\x12\x37\n\x14proxy_engine_request\x18\x01 \x01(\x0b\x32\x19.imrpc.ProxyEngineRequest\"\xf0\x01\n\x17\x45ngineReplicaAddRequest\x12\x37\n\x14proxy_engine_request\x18\x01 \x01(\x0b\x32\x19.imrpc.ProxyEngineRequest\x12\x17\n\x0freplica_address\x18\x02 \x01(\t\x12\x0f\n\x07restore\x18\x03 \x01(\x08\x12\x0c\n\x04size\x18\x04 \x01(\x03\x12\x14\n\x0c\x63urrent_size\x18\x05 \x01(\x03\x12\x11\n\tfast_sync\x18\x06 \x01(\x08\x12%\n\x1d\x66ile_sync_http_client_timeout\x18\x07 \x01(\x05\x12\x14\n\x0creplica_name\x18\x08 \x01(\t\"P\n\x1e\x45ngineReplicaListProxyResponse\x12.\n\x0creplica_list\x18\x01 \x01(\x0b\x32\x18.ptypes.ReplicaListReply\"\x8b\x01\n!EngineReplicaVerifyRebuildRequest\x12\x37\n\x14proxy_engine_request\x18\x01 \x01(\x0b\x32\x19.imrpc.ProxyEngineRequest\x12\x17\n\x0freplica_address\x18\x02 \x01(\t\x12\x14\n\x0creplica_name\x18\x03 \x01(\t\"\xca\x01\n\'EngineReplicaRebuildStatusProxyResponse\x12J\n\x06status\x18\x01 \x03(\x0b\x32:.imrpc.EngineReplicaRebuildStatusProxyResponse.StatusEntry\x1aS\n\x0bStatusEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x33\n\x05value\x18\x02 \x01(\x0b\x32$.ptypes.ReplicaRebuildStatusResponse:\x02\x38\x01\"\x84\x01\n\x1a\x45ngineReplicaRemoveRequest\x12\x37\n\x14proxy_engine_request\x18\x01 \x01(\x0b\x32\x19.imrpc.ProxyEngineRequest\x12\x17\n\x0freplica_address\x18\x02 \x01(\t\x12\x14\n\x0creplica_name\x18\x03 \x01(\t\"\x95\x01\n\x1e\x45ngineReplicaModeUpdateRequest\x12\x37\n\x14proxy_engine_request\x18\x01 \x01(\x0b\x32\x19.imrpc.ProxyEngineRequest\x12\x17\n\x0freplica_address\x18\x02 \x01(\t\x12!\n\x04mode\x18\x03 \x01(\x0e\x32\x13.ptypes.ReplicaMode\"{\n\x19\x45ngineSnapshotHashRequest\x12\x37\n\x14proxy_engine_request\x18\x01 \x01(\x0b\x32\x19.imrpc.ProxyEngineRequest\x12\x15\n\rsnapshot_name\x18\x02 \x01(\t\x12\x0e\n\x06rehash\x18\x03 \x01(\x08\"q\n\x1f\x45ngineSnapshotHashStatusRequest\x12\x37\n\x14proxy_engine_request\x18\x01 \x01(\x0b\x32\x19.imrpc.ProxyEngineRequest\x12\x15\n\rsnapshot_name\x18\x02 \x01(\t\"\xc4\x01\n%EngineSnapshotHashStatusProxyResponse\x12H\n\x06status\x18\x01 \x03(\x0b\x32\x38.imrpc.EngineSnapshotHashStatusProxyResponse.StatusEntry\x1aQ\n\x0bStatusEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x31\n\x05value\x18\x02 \x01(\x0b\x32\".ptypes.SnapshotHashStatusResponse:\x02\x38\x01\"A\n\x1d\x45ngineMetricsGetProxyResponse\x12 \n\x07metrics\x18\x01 \x01(\x0b\x32\x0f.ptypes.Metrics2\xb7\x15\n\x12ProxyEngineService\x12P\n\x10ServerVersionGet\x12\x19.imrpc.ProxyEngineRequest\x1a!.imrpc.EngineVersionProxyResponse\x12K\n\tVolumeGet\x12\x19.imrpc.ProxyEngineRequest\x1a#.imrpc.EngineVolumeGetProxyResponse\x12H\n\x0cVolumeExpand\x12 .imrpc.EngineVolumeExpandRequest\x1a\x16.google.protobuf.Empty\x12V\n\x13VolumeFrontendStart\x12\'.imrpc.EngineVolumeFrontendStartRequest\x1a\x16.google.protobuf.Empty\x12K\n\x16VolumeFrontendShutdown\x12\x19.imrpc.ProxyEngineRequest\x1a\x16.google.protobuf.Empty\x12t\n\"VolumeUnmapMarkSnapChainRemovedSet\x12\x36.imrpc.EngineVolumeUnmapMarkSnapChainRemovedSetRequest\x1a\x16.google.protobuf.Empty\x12\x62\n\x19VolumeSnapshotMaxCountSet\x12-.imrpc.EngineVolumeSnapshotMaxCountSetRequest\x1a\x16.google.protobuf.Empty\x12`\n\x18VolumeSnapshotMaxSizeSet\x12,.imrpc.EngineVolumeSnapshotMaxSizeSetRequest\x1a\x16.google.protobuf.Empty\x12^\n\x0eVolumeSnapshot\x12\".imrpc.EngineVolumeSnapshotRequest\x1a(.imrpc.EngineVolumeSnapshotProxyResponse\x12Q\n\x0cSnapshotList\x12\x19.imrpc.ProxyEngineRequest\x1a&.imrpc.EngineSnapshotListProxyResponse\x12L\n\x0eSnapshotRevert\x12\".imrpc.EngineSnapshotRevertRequest\x1a\x16.google.protobuf.Empty\x12J\n\rSnapshotPurge\x12!.imrpc.EngineSnapshotPurgeRequest\x1a\x16.google.protobuf.Empty\x12_\n\x13SnapshotPurgeStatus\x12\x19.imrpc.ProxyEngineRequest\x1a-.imrpc.EngineSnapshotPurgeStatusProxyResponse\x12J\n\rSnapshotClone\x12!.imrpc.EngineSnapshotCloneRequest\x1a\x16.google.protobuf.Empty\x12_\n\x13SnapshotCloneStatus\x12\x19.imrpc.ProxyEngineRequest\x1a-.imrpc.EngineSnapshotCloneStatusProxyResponse\x12L\n\x0eSnapshotRemove\x12\".imrpc.EngineSnapshotRemoveRequest\x1a\x16.google.protobuf.Empty\x12H\n\x0cSnapshotHash\x12 .imrpc.EngineSnapshotHashRequest\x1a\x16.google.protobuf.Empty\x12j\n\x12SnapshotHashStatus\x12&.imrpc.EngineSnapshotHashStatusRequest\x1a,.imrpc.EngineSnapshotHashStatusProxyResponse\x12^\n\x0eSnapshotBackup\x12\".imrpc.EngineSnapshotBackupRequest\x1a(.imrpc.EngineSnapshotBackupProxyResponse\x12p\n\x14SnapshotBackupStatus\x12(.imrpc.EngineSnapshotBackupStatusRequest\x1a..imrpc.EngineSnapshotBackupStatusProxyResponse\x12[\n\rBackupRestore\x12!.imrpc.EngineBackupRestoreRequest\x1a\'.imrpc.EngineBackupRestoreProxyResponse\x12_\n\x13\x42\x61\x63kupRestoreStatus\x12\x19.imrpc.ProxyEngineRequest\x1a-.imrpc.EngineBackupRestoreStatusProxyResponse\x12V\n\x13\x42\x61\x63kupRestoreFinish\x12\'.imrpc.EngineBackupRestoreFinishRequest\x1a\x16.google.protobuf.Empty\x12J\n\x18\x43leanupBackupMountPoints\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\x12\x44\n\nReplicaAdd\x12\x1e.imrpc.EngineReplicaAddRequest\x1a\x16.google.protobuf.Empty\x12O\n\x0bReplicaList\x12\x19.imrpc.ProxyEngineRequest\x1a%.imrpc.EngineReplicaListProxyResponse\x12\x64\n\x17ReplicaRebuildingStatus\x12\x19.imrpc.ProxyEngineRequest\x1a..imrpc.EngineReplicaRebuildStatusProxyResponse\x12X\n\x14ReplicaVerifyRebuild\x12(.imrpc.EngineReplicaVerifyRebuildRequest\x1a\x16.google.protobuf.Empty\x12J\n\rReplicaRemove\x12!.imrpc.EngineReplicaRemoveRequest\x1a\x16.google.protobuf.Empty\x12R\n\x11ReplicaModeUpdate\x12%.imrpc.EngineReplicaModeUpdateRequest\x1a\x16.google.protobuf.Empty\x12M\n\nMetricsGet\x12\x19.imrpc.ProxyEngineRequest\x1a$.imrpc.EngineMetricsGetProxyResponseB9Z7github.com/longhorn/longhorn-instance-manager/pkg/imrpcb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'github.com.longhorn.longhorn_instance_manager.pkg.imrpc.proxy_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z7github.com/longhorn/longhorn-instance-manager/pkg/imrpc'
  _PROXYENGINEREQUEST.fields_by_name['backend_store_driver']._options = None
  _PROXYENGINEREQUEST.fields_by_name['backend_store_driver']._serialized_options = b'\030\001'
  _ENGINESNAPSHOTLISTPROXYRESPONSE_DISKSENTRY._options = None
  _ENGINESNAPSHOTLISTPROXYRESPONSE_DISKSENTRY._serialized_options = b'8\001'
  _ENGINESNAPSHOTDISKINFO_CHILDRENENTRY._options = None
  _ENGINESNAPSHOTDISKINFO_CHILDRENENTRY._serialized_options = b'8\001'
  _ENGINESNAPSHOTDISKINFO_LABELSENTRY._options = None
  _ENGINESNAPSHOTDISKINFO_LABELSENTRY._serialized_options = b'8\001'
  _ENGINESNAPSHOTPURGESTATUSPROXYRESPONSE_STATUSENTRY._options = None
  _ENGINESNAPSHOTPURGESTATUSPROXYRESPONSE_STATUSENTRY._serialized_options = b'8\001'
  _ENGINESNAPSHOTCLONESTATUSPROXYRESPONSE_STATUSENTRY._options = None
  _ENGINESNAPSHOTCLONESTATUSPROXYRESPONSE_STATUSENTRY._serialized_options = b'8\001'
  _ENGINESNAPSHOTBACKUPREQUEST_LABELSENTRY._options = None
  _ENGINESNAPSHOTBACKUPREQUEST_LABELSENTRY._serialized_options = b'8\001'
  _ENGINEBACKUPRESTORESTATUSPROXYRESPONSE_STATUSENTRY._options = None
  _ENGINEBACKUPRESTORESTATUSPROXYRESPONSE_STATUSENTRY._serialized_options = b'8\001'
  _ENGINEREPLICAREBUILDSTATUSPROXYRESPONSE_STATUSENTRY._options = None
  _ENGINEREPLICAREBUILDSTATUSPROXYRESPONSE_STATUSENTRY._serialized_options = b'8\001'
  _ENGINESNAPSHOTHASHSTATUSPROXYRESPONSE_STATUSENTRY._options = None
  _ENGINESNAPSHOTHASHSTATUSPROXYRESPONSE_STATUSENTRY._serialized_options = b'8\001'
  _globals['_PROXYENGINEREQUEST']._serialized_start=311
  _globals['_PROXYENGINEREQUEST']._serialized_end=491
  _globals['_ENGINEVERSIONPROXYRESPONSE']._serialized_start=493
  _globals['_ENGINEVERSIONPROXYRESPONSE']._serialized_end=561
  _globals['_ENGINEVOLUMEGETPROXYRESPONSE']._serialized_start=563
  _globals['_ENGINEVOLUMEGETPROXYRESPONSE']._serialized_end=625
  _globals['_ENGINEVOLUMEEXPANDREQUEST']._serialized_start=628
  _globals['_ENGINEVOLUMEEXPANDREQUEST']._serialized_end=757
  _globals['_ENGINEVOLUMEFRONTENDSTARTREQUEST']._serialized_start=760
  _globals['_ENGINEVOLUMEFRONTENDSTARTREQUEST']._serialized_end=911
  _globals['_ENGINEVOLUMESNAPSHOTREQUEST']._serialized_start=914
  _globals['_ENGINEVOLUMESNAPSHOTREQUEST']._serialized_end=1056
  _globals['_ENGINEVOLUMESNAPSHOTPROXYRESPONSE']._serialized_start=1058
  _globals['_ENGINEVOLUMESNAPSHOTPROXYRESPONSE']._serialized_end=1140
  _globals['_ENGINEVOLUMEUNMAPMARKSNAPCHAINREMOVEDSETREQUEST']._serialized_start=1143
  _globals['_ENGINEVOLUMEUNMAPMARKSNAPCHAINREMOVEDSETREQUEST']._serialized_end=1325
  _globals['_ENGINEVOLUMESNAPSHOTMAXCOUNTSETREQUEST']._serialized_start=1328
  _globals['_ENGINEVOLUMESNAPSHOTMAXCOUNTSETREQUEST']._serialized_end=1482
  _globals['_ENGINEVOLUMESNAPSHOTMAXSIZESETREQUEST']._serialized_start=1485
  _globals['_ENGINEVOLUMESNAPSHOTMAXSIZESETREQUEST']._serialized_end=1636
  _globals['_ENGINESNAPSHOTLISTPROXYRESPONSE']._serialized_start=1639
  _globals['_ENGINESNAPSHOTLISTPROXYRESPONSE']._serialized_end=1815
  _globals['_ENGINESNAPSHOTLISTPROXYRESPONSE_DISKSENTRY']._serialized_start=1740
  _globals['_ENGINESNAPSHOTLISTPROXYRESPONSE_DISKSENTRY']._serialized_end=1815
  _globals['_ENGINESNAPSHOTDISKINFO']._serialized_start=1818
  _globals['_ENGINESNAPSHOTDISKINFO']._serialized_end=2160
  _globals['_ENGINESNAPSHOTDISKINFO_CHILDRENENTRY']._serialized_start=2066
  _globals['_ENGINESNAPSHOTDISKINFO_CHILDRENENTRY']._serialized_end=2113
  _globals['_ENGINESNAPSHOTDISKINFO_LABELSENTRY']._serialized_start=2115
  _globals['_ENGINESNAPSHOTDISKINFO_LABELSENTRY']._serialized_end=2160
  _globals['_ENGINESNAPSHOTREVERTREQUEST']._serialized_start=2162
  _globals['_ENGINESNAPSHOTREVERTREQUEST']._serialized_end=2262
  _globals['_ENGINESNAPSHOTPURGEREQUEST']._serialized_start=2264
  _globals['_ENGINESNAPSHOTPURGEREQUEST']._serialized_end=2378
  _globals['_ENGINESNAPSHOTPURGESTATUSPROXYRESPONSE']._serialized_start=2381
  _globals['_ENGINESNAPSHOTPURGESTATUSPROXYRESPONSE']._serialized_end=2580
  _globals['_ENGINESNAPSHOTPURGESTATUSPROXYRESPONSE_STATUSENTRY']._serialized_start=2498
  _globals['_ENGINESNAPSHOTPURGESTATUSPROXYRESPONSE_STATUSENTRY']._serialized_end=2580
  _globals['_ENGINESNAPSHOTCLONEREQUEST']._serialized_start=2583
  _globals['_ENGINESNAPSHOTCLONEREQUEST']._serialized_end=2850
  _globals['_ENGINESNAPSHOTCLONESTATUSPROXYRESPONSE']._serialized_start=2853
  _globals['_ENGINESNAPSHOTCLONESTATUSPROXYRESPONSE']._serialized_end=3052
  _globals['_ENGINESNAPSHOTCLONESTATUSPROXYRESPONSE_STATUSENTRY']._serialized_start=2970
  _globals['_ENGINESNAPSHOTCLONESTATUSPROXYRESPONSE_STATUSENTRY']._serialized_end=3052
  _globals['_ENGINESNAPSHOTREMOVEREQUEST']._serialized_start=3054
  _globals['_ENGINESNAPSHOTREMOVEREQUEST']._serialized_end=3155
  _globals['_ENGINESNAPSHOTBACKUPREQUEST']._serialized_start=3158
  _globals['_ENGINESNAPSHOTBACKUPREQUEST']._serialized_end=3578
  _globals['_ENGINESNAPSHOTBACKUPREQUEST_LABELSENTRY']._serialized_start=2115
  _globals['_ENGINESNAPSHOTBACKUPREQUEST_LABELSENTRY']._serialized_end=2160
  _globals['_ENGINESNAPSHOTBACKUPPROXYRESPONSE']._serialized_start=3580
  _globals['_ENGINESNAPSHOTBACKUPPROXYRESPONSE']._serialized_end=3675
  _globals['_ENGINESNAPSHOTBACKUPSTATUSREQUEST']._serialized_start=3678
  _globals['_ENGINESNAPSHOTBACKUPSTATUSREQUEST']._serialized_end=3838
  _globals['_ENGINESNAPSHOTBACKUPSTATUSPROXYRESPONSE']._serialized_start=3841
  _globals['_ENGINESNAPSHOTBACKUPSTATUSPROXYRESPONSE']._serialized_end=3998
  _globals['_ENGINEBACKUPRESTOREREQUEST']._serialized_start=4001
  _globals['_ENGINEBACKUPRESTOREREQUEST']._serialized_end=4176
  _globals['_ENGINEBACKUPRESTOREPROXYRESPONSE']._serialized_start=4178
  _globals['_ENGINEBACKUPRESTOREPROXYRESPONSE']._serialized_end=4231
  _globals['_ENGINEBACKUPRESTORESTATUSPROXYRESPONSE']._serialized_start=4234
  _globals['_ENGINEBACKUPRESTORESTATUSPROXYRESPONSE']._serialized_end=4430
  _globals['_ENGINEBACKUPRESTORESTATUSPROXYRESPONSE_STATUSENTRY']._serialized_start=4351
  _globals['_ENGINEBACKUPRESTORESTATUSPROXYRESPONSE_STATUSENTRY']._serialized_end=4430
  _globals['_ENGINEBACKUPRESTORESTATUS']._serialized_start=4433
  _globals['_ENGINEBACKUPRESTORESTATUS']._serialized_end=4625
  _globals['_ENGINEBACKUPRESTOREFINISHREQUEST']._serialized_start=4627
  _globals['_ENGINEBACKUPRESTOREFINISHREQUEST']._serialized_end=4718
  _globals['_ENGINEREPLICAADDREQUEST']._serialized_start=4721
  _globals['_ENGINEREPLICAADDREQUEST']._serialized_end=4961
  _globals['_ENGINEREPLICALISTPROXYRESPONSE']._serialized_start=4963
  _globals['_ENGINEREPLICALISTPROXYRESPONSE']._serialized_end=5043
  _globals['_ENGINEREPLICAVERIFYREBUILDREQUEST']._serialized_start=5046
  _globals['_ENGINEREPLICAVERIFYREBUILDREQUEST']._serialized_end=5185
  _globals['_ENGINEREPLICAREBUILDSTATUSPROXYRESPONSE']._serialized_start=5188
  _globals['_ENGINEREPLICAREBUILDSTATUSPROXYRESPONSE']._serialized_end=5390
  _globals['_ENGINEREPLICAREBUILDSTATUSPROXYRESPONSE_STATUSENTRY']._serialized_start=5307
  _globals['_ENGINEREPLICAREBUILDSTATUSPROXYRESPONSE_STATUSENTRY']._serialized_end=5390
  _globals['_ENGINEREPLICAREMOVEREQUEST']._serialized_start=5393
  _globals['_ENGINEREPLICAREMOVEREQUEST']._serialized_end=5525
  _globals['_ENGINEREPLICAMODEUPDATEREQUEST']._serialized_start=5528
  _globals['_ENGINEREPLICAMODEUPDATEREQUEST']._serialized_end=5677
  _globals['_ENGINESNAPSHOTHASHREQUEST']._serialized_start=5679
  _globals['_ENGINESNAPSHOTHASHREQUEST']._serialized_end=5802
  _globals['_ENGINESNAPSHOTHASHSTATUSREQUEST']._serialized_start=5804
  _globals['_ENGINESNAPSHOTHASHSTATUSREQUEST']._serialized_end=5917
  _globals['_ENGINESNAPSHOTHASHSTATUSPROXYRESPONSE']._serialized_start=5920
  _globals['_ENGINESNAPSHOTHASHSTATUSPROXYRESPONSE']._serialized_end=6116
  _globals['_ENGINESNAPSHOTHASHSTATUSPROXYRESPONSE_STATUSENTRY']._serialized_start=6035
  _globals['_ENGINESNAPSHOTHASHSTATUSPROXYRESPONSE_STATUSENTRY']._serialized_end=6116
  _globals['_ENGINEMETRICSGETPROXYRESPONSE']._serialized_start=6118
  _globals['_ENGINEMETRICSGETPROXYRESPONSE']._serialized_end=6183
  _globals['_PROXYENGINESERVICE']._serialized_start=6186
  _globals['_PROXYENGINESERVICE']._serialized_end=8929
# @@protoc_insertion_point(module_scope)
