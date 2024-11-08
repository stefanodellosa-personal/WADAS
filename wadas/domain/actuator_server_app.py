"""FASTAPI app for HTTPS Actuator Server"""

import json
import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from wadas.domain.actuator import Actuator

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/api/v1/actuators/{actuator_id}")
async def get_actuator_command(actuator_id: str):
    """Method to give a command to an actuator when requested."""
    logger.info("Connected remote actuator with ID: %s", actuator_id)

    if actuator_id in Actuator.actuators:
        cmd = Actuator.actuators[actuator_id].get_command()
        return JSONResponse(content=json.loads(cmd) if cmd else {"cmd": None}, status_code=200)

    else:
        logger.info("No actuator found with ID: %s", actuator_id)
        raise HTTPException(status_code=404, detail="Actuator does not exist")
