from pydantic import Field, AliasChoices, model_validator
from enum import Enum
from typing import Annotated
from annotated_types import Len
from app.base_schema import BaseSchema

class DestinationType(str, Enum):
    local = "local"
    volume = "volume"

class SourceType(str, Enum):
    blank = "blank"
    image = "image"
    snapshot = "snapshot"
    volume = "volume"

class Network(BaseSchema):
    uuid: str | None = None
    name: str | None = None
    port: str | None = None
    fixed_ip: str | None = None
    tag: str | None = None
    accessIPv4: str | None = None
    accessIPv6: str | None = None
    adminPass: str | None = None
    availability_zone: str | None = None

    @model_validator(mode='after')
    def validate_uuid(self):
        if not self.uuid and not self.name:
            raise ValueError("Either network uuid or name must be provided")
        return self

class BlockDeviceMappingV2(BaseSchema):
    boot_index: int | None = None
    delete_on_termination: bool = False
    destination_type: DestinationType = DestinationType.volume
    device_name: str | None = None
    device_type: str | None = None
    disk_bus: str | None = None
    guest_format: str | None = None
    no_device: bool | None = None
    source_type: SourceType | None = None
    uuid: str | None = None
    volume_size: int | None = None
    tag: str | None = None
    volume_type: str | None = None

    @model_validator(mode='after')
    def validate_source_type(self):
        if self.source_type is None and self.no_device == None:
            raise ValueError("Either 'source_type' or 'no_device' must be provided.")
        elif self.source_type != SourceType.blank and self.destination_type == DestinationType.local:
            raise ValueError("When 'destination_type' is 'local', 'source_type' cannot be image or snapshot or volume.")
        return self

class Server(BaseSchema):
    flavorRef: str
    name: str
    networks: list[Network] | str | None = "auto" or "none" or None     # destructive option, modify create new instance
    block_device_mapping_v2: list[BlockDeviceMappingV2] | None = None
    # config_drive: bool | None = None    # destructive option, modify create new instance
    imageRef: str | None = None     # destructive option, modify create new instance
    key_name: str | None = None     # destructive option, modify create new instance
    metadata: dict[str, str] | None = None
    # disk_config: str | None = Field(default=None, alias='OS-DCF:diskConfig')  # destructive option
    # personality: list[dict[str, str]] | None = None   # destructive option
    security_groups: list[str] | None = None
    user_data: str | None = None    # destructive option, modify create new instance
    description: str | None = None
    hostname: str | None = None
    tags: list[str] | None = None
    # trusted_image_certificates: Annotated[list[str] | None, Len(max_length=50)] = None    # destructive option
    # host: str | None = None   # destructive option
    # hypervisor_hostname: str | None = None    # destructive option

    @model_validator(mode='after')
    def validate_imageRef(self):
        if self.imageRef is None and not self.block_device_mapping_v2:
            raise ValueError("Either 'imageRef' or 'block_device_mapping_v2' must be provided.")
        return self

# # add field to exclude
# class ModifiedServer(Server):
#     class Config:
#         fields = {

#         }

class SchedulerHints(BaseSchema):
    build_near_host_ip: str | None = None
    cidr: str | None = None
    different_cell: list[str] | None = None
    different_host: list[str] | str | None = None
    group: str | None = None
    query: str | None = None
    same_host: list[str] | str | None = None
    target_cell: str | None = None

class ServerCreateRequest(BaseSchema):
    server: Server
    # scheduler_hints: SchedulerHints | None = Field(default=None, validation_alias=AliasChoices("os:scheduler_hints", "OS-SCH-HNT:scheduler_hints"))   # destructive option

class ServerUpdateRequest(BaseSchema):
    accessIPv4: str | None = None
    accessIPv6: str | None = None
    name: str | None = None
    hostname: str | None = None
    disk_config: str | None = Field(default=None, alias='OS-DCF:diskConfig')
    description: str | None = None

class ServerCreateImageRequest(BaseSchema):
    name: str
    metadata: dict[str, str] | None = None

class VolumeAttachment(BaseSchema):
    volumeId: str
    device: str | None = None
    tag: str | None = None
    delete_on_termination: bool = False

class VolumeAttachmentRequest(BaseSchema):
    volumeAttachment: VolumeAttachment