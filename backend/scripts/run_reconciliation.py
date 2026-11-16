from pathlib import Path

import pandas as pd
from app.services.persistence_service import persist_reconciliation
from app.services.reconciliation_service import reconcile_reports

BASE_DIR = Path(__file__).resolve().parents[2]

RECEIVED_PATH = BASE_DIR / "data" / "samples" / "received_report.csv"
DISPATCHED_PATH = BASE_DIR / "data" / "samples" / "dispatched_report.csv"


def main() -> None:
    received_df = pd.read_csv(RECEIVED_PATH)
    dispatched_df = pd.read_csv(DISPATCHED_PATH)

    reference_time = pd.Timestamp.now(tz="UTC")

    result = reconcile_reports(
        received_df,
        dispatched_df,
        reference_time,
        threshold_hours=24,
    )

    shipments = result["shipments"]

    saved_count = persist_reconciliation(
        shipment_df=shipments,
        received_file=RECEIVED_PATH,
        dispatched_file=DISPATCHED_PATH,
        received_row_count=len(received_df),
        dispatched_row_count=len(dispatched_df),
    )

    print("\nLOGFLOW AI - RECONCILIATION REPORT")
    print("=" * 45)

    print("\nShipment status:")
    print(shipments["status"].value_counts().to_string())

    print("\nData quality:")
    print(f"Duplicated received: {len(result['duplicates_received'])}")

    print(f"Duplicated dispatched: {len(result['duplicates_dispatched'])}")

    print(f"Invalid received: {len(result['invalid_received'])}")

    print(f"Invalid dispatched: {len(result['invalid_dispatched'])}")

    print(f"\nShipments processed: {saved_count}")
    print(f"Database: {BASE_DIR / 'data' / 'logflow.db'}")

    print("\nReconciliation and persistence completed!")


if __name__ == "__main__":
    main()
