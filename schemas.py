from pydantic import BaseModel

from waste_type_enum import WasteType


class MeasurementSchema(BaseModel):
    device_id: str
    user_id: str
    cooperative_id: str
    weight: float
    waste_type: WasteType
    timestamp: int

    # {"device_id": "1", "cooperative_id": "coop1", "weight": 150.8, "waste_type": "plastic", "user_id": "user1", "timestamp": 1730221393}
