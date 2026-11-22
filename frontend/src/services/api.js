const API_BASE_URL = "http://127.0.0.1:8001/api";

async function request(endpoint){
    const response = await fetch(`${API_BASE_URL}${endpoint}`)

    if(!response.ok){
        throw new Error(
            `Erro na requisição: ${response.status}`
        );
    }
    return response.json()
}

export function getShipments(){
    return request("/shipments");
}

export function getPendingShipments(){
    return request("/shipments/pending");
}

export function getDelayedShipments(){
    return request("/shipments/delayed");
}