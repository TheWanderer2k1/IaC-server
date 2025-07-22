from pydantic import Field, model_validator, AliasChoices
from app.base_schema import BaseSchema

class Volume(BaseSchema):
    size: int
    availability_zone: str | None = None
    source_volid: str | None = None
    description: str | None = None
    snapshot_id: str | None = None
    backup_id: str | None = None
    name: str | None = None
    imageRef: str | None = None 
    volume_type: str | None = None
    metadata: dict[str, str] | None = None
    consistencygroup_id: str | None = None

class SchedulerHints(BaseSchema):
    same_host: list[str]

class BlockVolumeCreateRequest(BaseSchema):
    volume: Volume
    # scheduler_hints: SchedulerHints | None = Field(default=None, validation_alias=AliasChoices("os:scheduler_hints", "OS-SCH-HNT:scheduler_hints"))   # destructive option

class VolumeAttach(BaseSchema):
    instance_uuid: str | None = None
    host_name: str | None = None
    mountpoint: str

    @model_validator(mode='after')
    def validate_imageRef(self):
        if self.instance_uuid is None and not self.host_name:
            raise ValueError("Either 'instane_uuid' or 'host_name' must be provided.")
        return self
    
class VolumeAttachRequest(BaseSchema):
    os_attach: VolumeAttach = Field(validation_alias=AliasChoices("os-attach"))

class VolumeDetach(BaseSchema):
    attachment_id: str | None = None

class VolumeDetachRequest(BaseSchema):
    os_detach: VolumeDetach = Field(validation_alias=AliasChoices("os-detach"))