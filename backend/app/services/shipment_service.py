from datetime import datetime, timedelta

from app.domain.shipment import Shipment
from app.repositories.shipment_repository import (
    list_shipments,
    list_shipments_by_status,
)
from sqlalchemy.orm import Session


def find_pending_shipments(
    shipments: list[Shipment],
) -> list[Shipment]:
    """
    Returns a list of pending shipments from the provided list of shipments.

    Args:
        shipments (list[Shipment]): A list of Shipment objects to filter.

    """
    return [shipment for shipment in shipments if shipment.is_pending]


def find_delayed_shipments(
    shipments: list[Shipment],
    reference_time: datetime,
    treshold_hours: int = 24,
) -> list[Shipment]:
    """
    Returns a list of delayed shipments from the provided list of shipments.

    A shipment is considered delayed if it has been received but not dispatched
    within the specified threshold hours from the reference time.

    Args:
        shipments (list[Shipment]): A list of Shipment objects to filter.
        reference_time (datetime): The reference time to compare against.
        treshold_hours (int): The number of hours after which a shipment is considered delayed.

    """
    if reference_time.tzinfo is None:
        raise ValueError("reference_time must be timezone-aware")
    if treshold_hours <= 0:
        raise ValueError("treshold_hours must be greater than zero")

    threshold = timedelta(hours=treshold_hours)

    return [
        shipment
        for shipment in shipments
        if (shipment.is_pending and reference_time - shipment.received_at > threshold)
    ]
    
def get_all_shipments(session: Session) -> list[Shipment]:
    return list_shipments(session)

def get_shipments_by_status(session: Session, status: str) -> list[Shipment]:
    return list_shipments_by_status(session, status)

