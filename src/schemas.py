import enum
from datetime import datetime

from pydantic import BaseModel


class WasteType(str, enum.Enum):
    PAPER = "paper"
    PLASTIC = "plastic"
    GLASS = "glass"
    METAL = "metal"
    ORGANIC = "organic"
    TEXTILE = "textile"
    OTHER = "other"


class MeasurementBaseSchema(BaseModel):
    device_id: str
    user_id: str
    cooperative_id: str
    weight: float
    waste_type: WasteType
    timestamp: int

    # {"device_id": "1", "cooperative_id": "coop1", "weight": 150.8, "waste_type": "plastic", "user_id": "user1", "timestamp": 1730221393}


class MeasurementSchema(MeasurementBaseSchema):
    id: str


class WastePriceSchema(BaseModel):
    id: str
    waste_type: WasteType
    price_per_kg: float
    date: datetime


class RoleEnum(str, enum.Enum):
    waste_picker = "waste_picker"
    cooperative_manager = "cooperative_manager"


class UserSchema(BaseModel):
    id: str
    name: str
    email: str
    role: RoleEnum
