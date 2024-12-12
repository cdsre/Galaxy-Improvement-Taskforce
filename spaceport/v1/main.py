from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import uuid
import uvicorn
import os

app = FastAPI()

class Ship(BaseModel):
    id: str
    authorization_code: str

DOCKING_LIMIT = int(os.getenv("DOCKING_LIMIT", 3))

docked_ships: List[Ship] = []
docking_requests: Dict[str, str] = {}  # ship_id -> authorization_code
separation_requests: Dict[str, str] = {}  # ship_id -> authorization_code

@app.get("/request_docking/{ship_id}")
def request_docking(ship_id: str):
    if len(docked_ships) + len(docking_requests) >= DOCKING_LIMIT:
        raise HTTPException(status_code=400, detail="Docking limit reached")
    authorization_code = str(uuid.uuid4())
    docking_requests[ship_id] = authorization_code
    return {"authorization_code": authorization_code}

@app.post("/dock")
def dock(ship: Ship):
    if ship.id not in docking_requests or docking_requests[ship.id] != ship.authorization_code:
        raise HTTPException(status_code=400, detail="Invalid authorization code")
    for docked_ship in docked_ships:
        if docked_ship.id == ship.id:
            raise HTTPException(status_code=400, detail="Ship already docked")
    docked_ships.append(ship)
    del docking_requests[ship.id]
    return {"message": "Ship docked successfully"}

@app.get("/request_separation/{ship_id}")
def request_separation(ship_id: str):
    authorization_code = str(uuid.uuid4())
    separation_requests[ship_id] = authorization_code
    return {"authorization_code": authorization_code}

@app.post("/separate")
def separate(ship: Ship):
    if ship.id not in separation_requests or separation_requests[ship.id] != ship.authorization_code:
        raise HTTPException(status_code=400, detail="Invalid authorization code")
    for docked_ship in docked_ships:
        if docked_ship.id == ship.id:
            docked_ships.remove(docked_ship)
            del separation_requests[ship.id]
            return {"message": "Ship separated successfully"}
    raise HTTPException(status_code=400, detail="Ship not found")

@app.get("/docked_ships")
def list_docked_ships():
    return [{"id": ship.id} for ship in docked_ships]

@app.get("/authorization_requests")
def list_authorization_requests():
    docking_list = [{"id": ship_id} for ship_id in docking_requests.keys()]
    separation_list = [{"id": ship_id} for ship_id in separation_requests.keys()]
    return {"docking_requests": docking_list, "separation_requests": separation_list}

@app.post("/clear_lists")
def clear_lists():
    docked_ships.clear()
    docking_requests.clear()
    separation_requests.clear()
    return {"message": "All lists cleared"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)