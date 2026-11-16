from hashlib import sha256
from pathlib import Path

from app.db.models.operation_unit import OperationUnit
from app.db.models.report_import import ReportImport
from app.db.models.shipment import Shipment
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_or_create_unit(
    session: Session,
    unit_name: str,
) -> OperationUnit:

    unit = session.scalar(select(OperationUnit).where(OperationUnit.name == unit_name))

    if unit is None:
        unit = OperationUnit(name=unit_name)
        session.add(unit)
        session.flush()

    return unit


def calculate_file_hash(file_path: Path) -> str:
    return sha256(file_path.read_bytes()).hexdigest()


def register_report_import(
    session: Session,
    file_path: Path,
    report_type: str,
    row_count: int,
) -> tuple[ReportImport, bool]:

    file_hash = calculate_file_hash(file_path)

    existing = session.scalar(
        select(ReportImport).where(ReportImport.file_hash == file_hash)
    )

    if existing is not None:
        return existing, False

    report = ReportImport(
        filename=file_path.name,
        file_hash=file_hash,
        report_type=report_type,
        row_count=row_count,
        operation_unit_id=None,
    )

    session.add(report)
    session.flush()

    return report, True


def upsert_shipments(
    session: Session,
    records: list[dict],
) -> int:

    for record in records:
        unit_name = record.get("unit_received") or record.get("unit_dispatched")

        if not unit_name:
            raise ValueError("Shipment must have an associated operation unit.")

        unit = get_or_create_unit(session, unit_name)

        shipment = session.scalar(
            select(Shipment).where(Shipment.tracking_code == record["tracking_code"])
        )

        values = {
            "operation_unit": unit,
            "received_at": record["received_at"],
            "dispatched_at": record["dispatched_at"],
            "status": record["status"],
            "is_delayed": bool(record["is_delayed"]),
        }

        if shipment is None:
            shipment = Shipment(
                tracking_code=record["tracking_code"],
                **values,
            )

            session.add(shipment)

        else:
            for field, value in values.items():
                setattr(shipment, field, value)

    session.flush()

    return len(records)
