from app.base_schema import BaseSchema

class InfraPreset1Request(BaseSchema):
    subnet_cidr: str
    external_network_id: str
    image_id: str
    vol_size: int
    flavor_id: str
