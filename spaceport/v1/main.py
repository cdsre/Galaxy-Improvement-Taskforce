from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pythonjsonlogger import jsonlogger
from typing import List, Dict
import uuid
import uvicorn
import os
import logging

# Configure JSON logging
logger = logging.getLogger()
if not logger.hasHandlers():
    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)

app = FastAPI()


class Ship(BaseModel):
    id: str
    authorization_code: str
    passengers: int


# Vars
DOCKING_LIMIT = int(os.getenv("DOCKING_LIMIT", 3))
docked_ships: List[Ship] = []
docking_requests: Dict[str, str] = {}  # ship_id -> authorization_code
separation_requests: Dict[str, str] = {}  # ship_id -> authorization_code

@app.get("/request_docking/{ship_id}")
def request_docking(ship_id: str):
    logger.info(f"Requesting docking for ship {ship_id}")
    authorization_code = str(uuid.uuid4())
    docking_requests[ship_id] = authorization_code
    return {"authorization_code": authorization_code}


@app.post("/dock")
def dock(ship: Ship):
    if ship.id not in docking_requests or docking_requests[ship.id] != ship.authorization_code:
        logger.error(f"Invalid authorization code for ship {ship.id}", extra={"ship_id": ship.id})
        raise HTTPException(status_code=400, detail="Invalid authorization code")
    for docked_ship in docked_ships:
        if docked_ship.id == ship.id:
            logger.error(f"Ship {ship.id} already docked", extra={"ship_id": ship.id})
            raise HTTPException(status_code=400, detail="Ship already docked")
    if len(docked_ships) >= DOCKING_LIMIT:
        logger.error(f"Docking limit '{DOCKING_LIMIT}' reached, Dock is full", extra={"ship_id": ship.id})
        raise HTTPException(status_code=400, detail="Docking limit reached")

    docked_ships.append(ship)
    del docking_requests[ship.id]
    logger.info(f"Ship {ship.id} docked successfully", extra={"ship_id": ship.id})
    return {"message": "Ship docked successfully"}


@app.get("/request_separation/{ship_id}")
def request_separation(ship_id: str):
    logger.info(f"Requesting separation for ship {ship_id}", extra={"ship_id": ship_id})
    authorization_code = str(uuid.uuid4())
    separation_requests[ship_id] = authorization_code
    return {"authorization_code": authorization_code}


@app.post("/separate")
def separate(ship: Ship):
    if ship.id not in separation_requests or separation_requests[ship.id] != ship.authorization_code:
        logger.error(f"Invalid authorization code for ship {ship.id}", extra={"ship_id": ship.id})
        raise HTTPException(status_code=400, detail="Invalid authorization code")
    for docked_ship in docked_ships:
        if docked_ship.id == ship.id:
            docked_ships.remove(docked_ship)
            del separation_requests[ship.id]
            logger.info(f"Ship {ship.id} separated successfully", extra={"ship_id": ship.id})
            return {"message": "Ship separated successfully"}
    logger.error(f"Ship {ship.id} not found", extra={"ship_id": ship.id})
    raise HTTPException(status_code=400, detail="Ship not found")


@app.get("/docked_ships")
def list_docked_ships():
    return [ship.id for ship in docked_ships]


@app.post("/clear_lists")
def clear_lists():
    docked_ships.clear()
    docking_requests.clear()
    separation_requests.clear()
    return {"message": "All lists cleared"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80, log_config="logging_config.json")
