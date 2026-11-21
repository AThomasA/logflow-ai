from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ShipmentResponse(BaseModel):
    id: int
    tracking_code: str
    operation_unit_id: int
    received_at: datetime | None
    dispatched_at: datetime | None
    status: str
    is_delayed: bool

    model_config = ConfigDict(from_attributes=True)