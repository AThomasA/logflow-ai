from typing import TYPE_CHECKING

from app.db.base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.db.models.report_import import ReportImport
    from app.db.models.shipment import Shipment


class OperationUnit(Base):
    __tablename__ = "operation_units"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    shipments: Mapped[list["Shipment"]] = relationship(back_populates="operation_unit")

    reports: Mapped[list["ReportImport"]] = relationship(
        back_populates="operation_unit"
    )
