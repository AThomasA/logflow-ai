from datetime import UTC, datetime

from app.db.models.operation_unit import OperationUnit
from app.db.models.report_import import ReportImport
from app.db.models.shipment import Shipment
from app.repositories.shipment_repository import (
    list_shipments,
    list_shipments_by_status,
    register_report_import,
    upsert_shipments,
)
from sqlalchemy import func, select


def make_shipment(
    tracking_code="BR1001",
    status="pending",
):
    return {
        "tracking_code": tracking_code,
        "unit_received": "João Pessoa",
        "unit_dispatched": None,
        "received_at": datetime(2026, 11, 14, 9, 0, tzinfo=UTC),
        "dispatched_at": None,
        "status": status,
        "is_delayed": False,
    }


def test_save_shipment(db_session):
    upsert_shipments(
        db_session,
        [make_shipment()],
    )

    shipment = db_session.scalar(
        select(Shipment).where(Shipment.tracking_code == "BR1001")
    )

    assert shipment is not None
    assert shipment.status == "pending"
    assert shipment.operation_unit.name == "João Pessoa"


def test_list_shipments_in_id_order(db_session):
    upsert_shipments(
        db_session,
        [
            make_shipment("BR1002"),
            make_shipment("BR1001"),
        ],
    )

    shipments = list_shipments(db_session)

    assert [shipment.tracking_code for shipment in shipments] == ["BR1002", "BR1001"]


def test_list_shipments_by_status(db_session):
    upsert_shipments(
        db_session,
        [
            make_shipment("BR1001", status="pending"),
            make_shipment("BR1002", status="delayed"),
        ],
    )

    pending = list_shipments_by_status(db_session, "pending")
    delayed = list_shipments_by_status(db_session, "delayed")

    assert [shipment.tracking_code for shipment in pending] == ["BR1001"]
    assert [shipment.tracking_code for shipment in delayed] == ["BR1002"]


def test_create_operation_unit_only_once(db_session):
    upsert_shipments(
        db_session,
        [
            make_shipment("BR1001"),
            make_shipment("BR1002"),
        ],
    )

    unit_count = db_session.scalar(select(func.count()).select_from(OperationUnit))

    assert unit_count == 1


def test_upsert_does_not_duplicate_shipment(db_session):
    upsert_shipments(
        db_session,
        [make_shipment(status="pending")],
    )

    upsert_shipments(
        db_session,
        [make_shipment(status="delayed")],
    )

    shipment_count = db_session.scalar(select(func.count()).select_from(Shipment))

    shipment = db_session.scalar(
        select(Shipment).where(Shipment.tracking_code == "BR1001")
    )

    assert shipment_count == 1
    assert shipment.status == "delayed"


def test_report_import_is_idempotent(db_session, tmp_path):
    report_path = tmp_path / "received.csv"
    report_path.write_text(
        "tracking_code,unit\nBR1001,João Pessoa\n",
        encoding="utf-8",
    )

    first_import, first_created = register_report_import(
        db_session,
        report_path,
        "received",
        1,
    )

    second_import, second_created = register_report_import(
        db_session,
        report_path,
        "received",
        1,
    )

    report_count = db_session.scalar(select(func.count()).select_from(ReportImport))

    assert first_created is True
    assert second_created is False
    assert first_import.id == second_import.id
    assert report_count == 1
