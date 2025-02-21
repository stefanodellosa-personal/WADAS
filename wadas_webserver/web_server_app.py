# This file is part of WADAS project.
#
# WADAS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WADAS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WADAS. If not, see <https://www.gnu.org/licenses/>.
#
# Author(s): Stefano Dell'Osa, Alessandro Palla, Cesare Di Mauro, Antonio Farina
# Date: 2025-02-21
# Description: Module containing FastAPI exposed endpoints.
import logging
import os
from pathlib import Path
from typing import Annotated

import bcrypt
from fastapi import FastAPI, Header, HTTPException, Query, status
from jose import JWTError, jwt
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from wadas_webserver.database import Database
from wadas_webserver.server_config import ServerConfig
from wadas_webserver.utils import create_access_token, create_refresh_token
from wadas_webserver.view_model import (
    ActuationsRequest,
    DataResponse,
    DetectionsRequest,
    LoginRequest,
    PaginatedResponse,
    RefreshResponse,
    RefreshTokenRequest,
    User,
)

logger = logging.getLogger(__name__)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_token(token, token_type="access") -> User:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    try:
        payload = jwt.decode(
            token,
            (
                ServerConfig.instance.access_secret_key
                if token_type == "access"
                else ServerConfig.instance.refresh_secret_key
            ),
            algorithms=[ServerConfig.JWT_ENC_ALGORITHM],
        )

        if (username := payload.get("sub")) is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        if user := Database.instance.get_user_by_username(username):
            return user
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    except JWTError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@app.post("/api/v1/login")
async def login(data: LoginRequest):
    """Method to submit the login request"""
    if user := Database.instance.get_user_by_username(data.username):
        if bcrypt.checkpw(data.password.encode("utf-8"), user.password.encode("utf-8")):
            acc_token = create_access_token(data={"sub": data.username})
            ref_token = create_refresh_token(data={"sub": data.username})

            logger.info("User %s logged in.", user.username)

            return {
                "access_token": acc_token,
                "refresh_token": ref_token,
                "token_type": "JWT",
            }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )


@app.post("/api/v1/token/refresh")
async def refresh_token(request: RefreshTokenRequest):
    """Method to refresh access token using the refresh token"""
    user = verify_token(request.refresh_token, token_type="refresh")
    new_access_token = create_access_token(data={"sub": user.username})
    return RefreshResponse(access_token=new_access_token)


@app.get("/api/v1/cameras")
async def get_cameras(x_access_token: Annotated[str | None, Header()] = None):
    """Method to get all enabled cameras"""
    verify_token(x_access_token)
    cameras = Database.instance.get_cameras()
    return DataResponse(data=cameras)


@app.get("/api/v1/animals")
async def get_animals(x_access_token: Annotated[str | None, Header()] = None):
    """Method to get all known animals in the database"""
    verify_token(x_access_token)
    animals_names = Database.instance.get_known_animals()
    return DataResponse(data=animals_names)


@app.get("/api/v1/actuator_types")
async def get_actuator_types(x_access_token: Annotated[str | None, Header()] = None):
    """Method to get all known types for actuator"""
    verify_token(x_access_token)
    actuator_types = Database.instance.get_known_actuator_types()
    return DataResponse(data=actuator_types)


@app.get("/api/v1/actuation_commands")
async def get_actuation_commands(x_access_token: Annotated[str | None, Header()] = None):
    """Method to get all known commands for actuation events"""
    verify_token(x_access_token)
    actuation_commands = Database.instance.get_known_actuation_commands()
    return DataResponse(data=actuation_commands)


@app.get("/api/v1/detections")
async def get_filtered_detections(
    detection_filter: Annotated[DetectionsRequest, Query()],
    x_access_token: Annotated[str | None, Header()] = None,
):
    """Method to get paginated detection events filtered
    by different filters and their total count
    """
    verify_token(x_access_token)
    total, events = Database.instance.get_detection_events_by_filter(**detection_filter.__dict__)
    return PaginatedResponse(total=total, count=len(events), data=events)


@app.get("/api/v1/actuations")
async def get_filtered_actuations(
    actuation_filter: Annotated[ActuationsRequest, Query()],
    x_access_token: Annotated[str | None, Header()] = None,
):
    """Method to get paginated actuation events filtered
    by different filters and their total count
    """
    verify_token(x_access_token)
    total, events = Database.instance.get_actuation_events_by_filter(**actuation_filter.__dict__)
    return PaginatedResponse(total=total, count=len(events), data=events)


@app.get("/api/v1/detections/{event_id}/image")
async def download_image(
    event_id: int,
    x_access_token: Annotated[str | None, Header()] = None,
):
    """Method used to download the image (detection or classification)
    associated to the detection event
    """
    verify_token(x_access_token)
    event = Database.instance.get_detection_event_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    image_path = Path(ServerConfig.WADAS_ROOT_DIR) / (
        event.classification_img_path or event.detection_img_path
    )

    if (ext := image_path.suffix) == ".png":
        media_type = "image/png"
    elif ext in [".jpg", ".jpeg"]:
        media_type = "image/jpeg"
    else:
        logger.error("Image extension unknown for %s", image_path)
        raise HTTPException(status_code=500, detail="Generic Error")

    if not os.path.isfile(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(image_path, media_type=media_type, filename=f"{event_id}{ext}")


# Static pages mounted under the site root
app.mount(
    "/",
    StaticFiles(
        directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend"), html=True
    ),
    name="frontend",
)
