from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from random import randint
import requests
import socket

app = FastAPI()
SHIP_ID = socket.gethostname()

class Ship(BaseModel):
    id: str = SHIP_ID
    authorization_code: str = None
    passengers: int


def request_authorization(spaceport: str, endpoint: str):
    response = requests.get(f"http://{spaceport}/{endpoint}/{SHIP_ID}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json().get("authorization_code")

def perform_action(spaceport: str, endpoint: str, authorization_code: str):
    ship: Ship = Ship(authorization_code=authorization_code, passengers=randint(2, 2000))
    response = requests.post(f"http://{spaceport}/{endpoint}", json=ship.model_dump())
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

@app.post("/dock/{spaceport}")
def dock(spaceport: str):
    authorization_code = request_authorization(spaceport, "request_docking")
    return perform_action(spaceport, "dock", authorization_code)

@app.post("/separate/{spaceport}")
def separate(spaceport: str):
    authorization_code = request_authorization(spaceport, "request_separation")
    return perform_action(spaceport, "separate", authorization_code)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)