from app.base_schema import BaseSchema

class InfraPreset1Request(BaseSchema):
    subnet_cidr: str
    image_id: str
    flavor_id: str
    vol_size: int
