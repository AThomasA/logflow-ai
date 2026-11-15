import pandas as pd
import pytest
from app.services.reconciliation_service import reconcile_reports

REFERENCE_TIME = pd.Timestamp("2026-11-14T12:00:00Z")


def test_identifies_pending_and_dispatched_shipments():
    received = pd.DataFrame(
        [
            {
                "tracking_code": "BR1001",
                "unit": "João Pessoa",
                "received_at": "2026-11-14T09:00:00Z",
            },
            {
                "tracking_code": "BR1002",
                "unit": "Recife",
                "received_at": "2026-11-14T10:00:00Z",
            },
        ]
    )

    dispatched = pd.DataFrame(
        [
            {
                "tracking_code": "BR1001",
                "unit": "João Pessoa",
                "dispatched_at": "2026-11-14T11:00:00Z",
            },
        ]
    )

    result = reconcile_reports(
        received,
        dispatched,
        REFERENCE_TIME,
    )

    shipments = result["shipments"].set_index("tracking_code")

    assert shipments.loc["BR1001", "status"] == "dispatched"
    assert shipments.loc["BR1002", "status"] == "pending"


def test_identifies_delayed_shipment():
    received = pd.DataFrame(
        [
            {
                "tracking_code": "BR1001",
                "unit": "João Pessoa",
                "received_at": "2026-11-13T10:00:00Z",
            },
        ]
    )

    dispatched = pd.DataFrame(
        columns=[
            "tracking_code",
            "unit",
            "dispatched_at",
        ]
    )

    result = reconcile_reports(
        received,
        dispatched,
        REFERENCE_TIME,
    )

    shipment = result["shipments"].iloc[0]

    assert shipment["status"] == "delayed"
    assert shipment["is_delayed"] is True or shipment["is_delayed"] == True


def test_identifies_dispatch_without_receipt():
    received = pd.DataFrame(
        columns=[
            "tracking_code",
            "unit",
            "received_at",
        ]
    )

    dispatched = pd.DataFrame(
        [
            {
                "tracking_code": "BR9999",
                "unit": "Recife",
                "dispatched_at": "2026-11-14T11:00:00Z",
            },
        ]
    )

    result = reconcile_reports(
        received,
        dispatched,
        REFERENCE_TIME,
    )

    shipment = result["shipments"].iloc[0]

    assert shipment["status"] == "dispatch_without_receipt"


def test_identifies_duplicate_and_invalid_records():
    received = pd.DataFrame(
        [
            {
                "tracking_code": "BR1001",
                "unit": "João Pessoa",
                "received_at": "2026-11-14T09:00:00Z",
            },
            {
                "tracking_code": "BR1001",
                "unit": "João Pessoa",
                "received_at": "2026-11-14T09:30:00Z",
            },
            {
                "tracking_code": None,
                "unit": "Recife",
                "received_at": "2026-11-14T10:00:00Z",
            },
        ]
    )

    dispatched = pd.DataFrame(
        columns=[
            "tracking_code",
            "unit",
            "dispatched_at",
        ]
    )

    result = reconcile_reports(
        received,
        dispatched,
        REFERENCE_TIME,
    )

    assert len(result["duplicates_received"]) == 2
    assert len(result["invalid_received"]) == 1
    assert len(result["shipments"]) == 1


def test_identifies_unit_mismatch():
    received = pd.DataFrame(
        [
            {
                "tracking_code": "BR1001",
                "unit": "João Pessoa",
                "received_at": "2026-11-14T09:00:00Z",
            },
        ]
    )

    dispatched = pd.DataFrame(
        [
            {
                "tracking_code": "BR1001",
                "unit": "Recife",
                "dispatched_at": "2026-11-14T11:00:00Z",
            },
        ]
    )

    result = reconcile_reports(
        received,
        dispatched,
        REFERENCE_TIME,
    )

    assert result["shipments"].iloc[0]["status"] == "unit_mismatch"


def test_rejects_report_with_missing_columns():
    received = pd.DataFrame(
        [
            {
                "tracking_code": "BR1001",
                "unit": "João Pessoa",
            },
        ]
    )

    dispatched = pd.DataFrame(
        columns=[
            "tracking_code",
            "unit",
            "dispatched_at",
        ]
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        reconcile_reports(
            received,
            dispatched,
            REFERENCE_TIME,
        )


def test_exactly_24_hours_is_not_delayed():
    received = pd.DataFrame(
        [
            {
                "tracking_code": "BR1001",
                "unit": "João Pessoa",
                "received_at": "2026-11-13T12:00:00Z",
            },
        ]
    )

    dispatched = pd.DataFrame(
        columns=[
            "tracking_code",
            "unit",
            "dispatched_at",
        ]
    )

    result = reconcile_reports(
        received,
        dispatched,
        REFERENCE_TIME,
        threshold_hours=24,
    )

    assert result["shipments"].iloc[0]["status"] == "pending"
