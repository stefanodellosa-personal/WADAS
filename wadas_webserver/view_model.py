from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# Request Models
class RefreshTokenRequest(BaseModel):
    refresh_token: str


class LoginRequest(BaseModel):
    username: str
    password: str


class DetectionsRequest(BaseModel):
    camera_ids: Optional[List[int]] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    classified_animals: Optional[List[str]] = None
    order_by: Optional[str] = "timestamp_desc"
    offset: Optional[int] = 0
    limit: Optional[int] = 20


class ActuationsRequest(BaseModel):
    detection_id: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    actuator_types: Optional[List[str]] = None
    commands: Optional[List[str]] = None
    offset: Optional[int] = 0
    limit: Optional[int] = 20


# View Models
class User(BaseModel):
    username: str
    password: str
    email: str
    role: str


class Actuator(BaseModel):
    id: int
    name: str
    type: str


class Camera(BaseModel):
    id: int
    name: str
    type: str
    enabled: bool
    actuators: Optional[List[Actuator]] = []


class ClassifiedAnimal(BaseModel):
    animal: str
    probability: float


class DetectionEvent(BaseModel):
    id: int
    camera_id: int
    detection_img_path: Optional[str]
    classification_img_path: Optional[str]
    detected_animals: int
    classification: bool
    classified_animals: Optional[List[ClassifiedAnimal]]
    timestamp: datetime


class ActuationEvent(BaseModel):
    actuator: Actuator
    detection_event_id: int
    command: str
    timestamp: datetime


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "JWT"


class DataResponse(BaseModel):
    data: object


class PaginatedResponse(BaseModel):
    total: int
    count: int
    data: object
