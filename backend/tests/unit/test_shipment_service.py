from datetime import UTC, datetime

from app.domain.shipment import Shipment
from app.services.shipment_service import find_delayed_shipments, find_pending_shipments


def test_find_pending_shipments():
    shipments = [
        Shipment(
            tracking_code="BR1003",
            unit="joão pessoa",
            received_at=datetime(26, 11, 13, 9, 0, tzinfo=UTC),
        ),
        Shipment(
            tracking_code="BR1004",
            unit="recife",
            received_at=datetime(26, 11, 13, 10, 0, tzinfo=UTC),
            dispatched_at=datetime(26, 11, 13, 14, 0, tzinfo=UTC),
        ),
    ]

    pending = find_pending_shipments(shipments)

    assert len(pending) == 1
    assert pending[0].tracking_code == "BR1003"


def test_find_delayed_shipments():
    shipments = [
        Shipment(
            tracking_code="BR1001",
            unit="joão pessoa",
            received_at=datetime(26, 11, 13, 10, 0, tzinfo=UTC),
        ),
        Shipment(
            tracking_code="BR1002",
            unit="recife",
            received_at=datetime(26, 11, 14, 10, 0, tzinfo=UTC),
        ),
    ]

    reference_time = datetime(26, 11, 14, 11, 0, tzinfo=UTC)

    delayed = find_delayed_shipments(shipments, reference_time)

    assert len(delayed) == 1
    assert delayed[0].tracking_code == "BR1001"


def test_exactly_24hours_is_not_delayed():
    shipment = Shipment(
        tracking_code="BR1003",
        unit="recife",
        received_at=datetime(26, 11, 13, 10, 0, tzinfo=UTC),
    )

    reference_time = datetime(26, 11, 14, 10, 0, tzinfo=UTC)

    delayed = find_delayed_shipments([shipment], reference_time)

    assert delayed == []


def test_custom_delay_treshold():
    shipment = Shipment(
        tracking_code="BR1004",
        unit="joão pessoa",
        received_at=datetime(26, 11, 14, 8, 0, tzinfo=UTC),
    )

    reference_time = datetime(26, 11, 14, 18, 0, tzinfo=UTC)

    delayed = find_delayed_shipments([shipment], reference_time, treshold_hours=8)

    assert len(delayed) == 1
