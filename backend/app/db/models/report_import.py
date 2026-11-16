from datetime import UTC, datetime
from typing import TYPE_CHECKING

from app.db.base import Base
from app.db.types import UTCDateTime
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.db.models.operation_unit import OperationUnit


class ReportImport(Base):
    __tablename__ = "report_imports"

    id: Mapped[int] = mapped_column(primary_key=True)

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_hash: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
    )

    report_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    imported_at: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    row_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    operation_unit_id: Mapped[int | None] = mapped_column(
        ForeignKey("operation_units.id"),
        nullable=True,
    )

    operation_unit: Mapped["OperationUnit"] = relationship(back_populates="reports")
