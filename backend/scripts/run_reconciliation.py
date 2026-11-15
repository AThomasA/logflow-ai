import pandas as pd

from backend.app.services.reconciliation_service import reconcile_reports


def main() -> None:
    received_path = "data/samples/received_report.csv"
    dispatched_path = "data/samples/dispatched_report.csv"

    received_df = pd.read_csv(received_path)
    dispatched_df = pd.read_csv(dispatched_path)

    reference_time = pd.Timestamp.now(tz="UTC")

    result = reconcile_reports(
        received_df,
        dispatched_df,
        reference_time,
        threshold_hours=24,
    )

    shipments = result["shipments"]

    print("\nLOGFLOW AI - RECONCILIATION REPORT")
    print("=" * 40)

    print("\nShipment status:")
    print(shipments["status"].value_counts().to_string())

    print("\nData quality:")
    print(f"Duplicated received: {len(result['duplicates_dispatched'])}")

    print(f"Invalid received: {len(result['invalid_received'])}")

    print(f"Invalid dispatched: {len(result['invalid_dispatched'])}")

    print("\nReconciliation completed!")


if __name__ == "__main__":
    main()
