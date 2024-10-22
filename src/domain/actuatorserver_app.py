"""FASTAPI app for HTTPS Actuator Server"""

import json
import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from domain.actuator import Actuator

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/api/v1/actuators/{actuator_id}")
async def get_actuator_command(actuator_id: str):
    logger.info(f"Connected remote actuator with ID: {actuator_id}")

    if actuator_id in Actuator.actuators_pool:
        msg = Actuator.actuators_pool[actuator_id].get_command()
        if msg:
            return JSONResponse(content=json.loads(msg), status_code=200)
        else:
            return JSONResponse(content={"msg": None}, status_code=200)
    else:
        raise HTTPException(status_code=404, detail="Record does not exist")
