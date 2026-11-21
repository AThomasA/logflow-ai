from app.db.session import SessionLocal, create_tables
from app.schemas.shipment import ShipmentResponse
from app.services.shipment_service import (
    get_all_shipments,
    get_shipments_by_status,
)
from fastapi import FastAPI

create_tables()

app = FastAPI(
    title="LogFlow AI",
    description="API para automação e reconciliação logística.",
    version="0.1.0",
     
)

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "aplication": "LogFlow AI"
    }
    
@app.get(
    "/api/shipments", 
    response_model=list[ShipmentResponse],
)
def list_all_shipments():
    
    with SessionLocal() as session:
        shipments = get_all_shipments(session)
        
    return shipments


@app.get(
    "/api/shipments/pending", 
    response_model=list[ShipmentResponse],
)
def list_pending_shipments():
    
    with SessionLocal() as session:
        return get_shipments_by_status(session, "pending")
        

@app.get(
    "/api/shipments/delayed", 
    response_model=list[ShipmentResponse],
)
def list_delayed_shipments():
    
    with SessionLocal() as session:
        return get_shipments_by_status(session, "delayed")