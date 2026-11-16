from datetime import datetime
from typing import TYPE_CHECKING

from app.db.base import Base
from app.db.types import UTCDateTime
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.db.models.operation_unit import OperationUnit


class Shipment(Base):
    __tablename__ = "shipments"

    id: Mapped[int] = mapped_column(primary_key=True)

    tracking_code: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    operation_unit_id: Mapped[int] = mapped_column(
        ForeignKey("operation_units.id"),
        nullable=False,
    )

    received_at: Mapped[datetime | None] = mapped_column(
        UTCDateTime(),
        nullable=True,
    )

    dispatched_at: Mapped[datetime | None] = mapped_column(
        UTCDateTime(),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    is_delayed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    operation_unit: Mapped["OperationUnit"] = relationship(back_populates="shipments")
