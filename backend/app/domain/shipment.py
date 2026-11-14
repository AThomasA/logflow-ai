from dataclasses import dataclass
from datetime import datetime


@dataclass
class Shipment:
    tracking_code: str
    unit: str
    received_at: datetime
    dispatched_at: datetime | None = None

    def __post_init__(self):
        if not self.tracking_code.strip():
            raise ValueError("Tracking code cannot be empty.")

        if not self.unit.strip():
            raise ValueError("Unit cannot be empty.")

        if self.received_at.tzinfo is None:
            raise ValueError("received_at must be timezone-aware")

        if self.dispatched_at is not None:
            if self.dispatched_at.tzinfo is None:
                raise ValueError("dispatched_at must be timezone-aware")
            if self.dispatched_at < self.received_at:
                raise ValueError("dispatched_at cannot be earlier than received_at.")

    @property
    def is_pending(self) -> bool:
        return self.dispatched_at is None

    @property
    def status(self) -> str:
        return "received" if self.is_pending else "dispatched"
