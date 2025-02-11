import logging
import os
from typing import Annotated

import bcrypt
from fastapi import FastAPI, Header, HTTPException, Query, status
from jose import JWTError, jwt
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from wadas_webserver.config import ALGORITHM, REFRESH_SECRET_KEY, SECRET_KEY
from wadas_webserver.database import Database
from wadas_webserver.utils import create_access_token, create_refresh_token
from wadas_webserver.view_model import (
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
            SECRET_KEY if token_type == "access" else REFRESH_SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user = Database.instance.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        return user
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


# Static pages mounted under the site root
app.mount(
    "/",
    StaticFiles(
        directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend"), html=True
    ),
    name="frontend",
)
