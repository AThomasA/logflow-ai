from datetime import datetime, timezone, UTC
import pytest
from app.domain.shipment import Shipment

def test_create_shipment():
    shipment = Shipment(
        tracking_code = "BR1001",
        unit = "joão pessoa",
        received_at = datetime(
            26, 11, 13, 9, 0, tzinfo=UTC
        ),
    )
    
    assert shipment.tracking_code == "BR1001"
    assert shipment.unit == "joão pessoa"
    assert shipment.is_pending is True
    assert shipment.status == "received"
    
def test_dispatched_shipment():
    shipment = Shipment(
        tracking_code = "BR1002",
        unit = "recife",
        received_at = datetime(
            26, 11, 13, 10, 0, tzinfo=UTC
        ),
        dispatched_at = datetime(
            26, 11, 13, 14, 0, tzinfo=UTC
        ),
    )
    
    assert shipment.tracking_code =="BR1002"
    assert shipment.unit == "recife"
    assert shipment.is_pending is False
    assert shipment.status =="dispatched"
    
def test_tracking_code_cannot_be_empty():
    with pytest.raises(ValueError):
        Shipment(
            tracking_code = " ",
            unit = "joao pessoa",
            received_at = datetime(
                26, 11, 13, 9, 0, tzinfo=UTC
            ),
        )
        
def test_dispatch_cannot_be_before_receipt():
    with pytest.raises(ValueError):
        Shipment(
            tracking_code = "BR1003",
            unit = "joao pessoa",
            received_at = datetime(
                26, 11, 13, 9, 0, tzinfo=UTC
            ),
            dispatched_at = datetime(
                26, 11, 13, 8, 0, tzinfo=UTC
            ),
        )