from datetime import UTC, datetime
from pathlib import Path

import pandas as pd
from app.db.session import SessionLocal, create_tables
from app.repositories.shipment_repository import (
    register_report_import,
    upsert_shipments,
)


def clean_datetime(value) -> datetime | None:
    if pd.isna(value):
        return None

    if isinstance(value, pd.Timestamp):
        value = value.to_pydatetime()

    if value.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")

    return value.astimezone(UTC)


def dataframe_to_records(
    dataframe: pd.DataFrame,
) -> list[dict]:

    records = []

    for row in dataframe.to_dict(orient="records"):
        unit_received = row["unit_received"]
        unit_dispatched = row["unit_dispatched"]

        if pd.isna(unit_received):
            unit_received = None

        if pd.isna(unit_dispatched):
            unit_dispatched = None

        records.append(
            {
                "tracking_code": row["tracking_code"],
                "unit_received": unit_received,
                "unit_dispatched": unit_dispatched,
                "received_at": clean_datetime(row["received_at"]),
                "dispatched_at": clean_datetime(row["dispatched_at"]),
                "status": row["status"],
                "is_delayed": bool(row["is_delayed"]),
            }
        )

    return records


def persist_reconciliation(
    shipment_df: pd.DataFrame,
    received_file: Path,
    dispatched_file: Path,
    received_row_count: int,
    dispatched_row_count: int,
) -> int:

    create_tables()

    records = dataframe_to_records(shipment_df)

    with SessionLocal.begin() as session:
        register_report_import(
            session,
            received_file,
            "received",
            received_row_count,
        )

        register_report_import(
            session,
            dispatched_file,
            "dispatched",
            dispatched_row_count,
        )

        saved_count = upsert_shipments(
            session,
            records,
        )

    return saved_count
