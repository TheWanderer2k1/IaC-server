from app.base_schema import BaseSchema

class InfraPreset1Request(BaseSchema):
    subnet_cidr: str
    flavor_id: str
    base_vol_id: str
    vol_size: int
