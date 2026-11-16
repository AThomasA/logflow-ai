from app.db.models.operation_unit import OperationUnit
from app.db.models.report_import import ReportImport
from app.db.models.shipment import Shipment
from app.db.session import SessionLocal, create_tables
from sqlalchemy import func, select


def main() -> None:
    create_tables()

    with SessionLocal() as session:
        unit_count = session.scalar(select(func.count()).select_from(OperationUnit))

        shipment_count = session.scalar(select(func.count()).select_from(Shipment))

        report_count = session.scalar(select(func.count()).select_from(ReportImport))

        print("\nLOGFLOW AI - DATABASE INSPECTION")
        print("=" * 40)

        print(f"Operation units: {unit_count}")
        print(f"Shipments: {shipment_count}")
        print(f"Imported reports: {report_count}")

        print("\nOperation units:")

        units = session.scalars(
            select(OperationUnit).order_by(OperationUnit.name)
        ).all()

        for unit in units:
            print(f"- {unit.name}")

        print("\nShipments:")

        shipments = session.scalars(
            select(Shipment).order_by(Shipment.tracking_code)
        ).all()

        for shipment in shipments[:10]:
            print(
                f"{shipment.tracking_code} | "
                f"{shipment.operation_unit.name} | "
                f"{shipment.status}"
            )

        print("\nImported reports:")

        reports = session.scalars(select(ReportImport).order_by(ReportImport.id)).all()

        for report in reports:
            print(f"{report.filename} | {report.report_type} | {report.row_count} rows")


if __name__ == "__main__":
    main()
