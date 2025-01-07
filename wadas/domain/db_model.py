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
# Date: 2025-01-04
# Description: database model module, it contains ORM classes.

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

from wadas._version import __dbversion__
from wadas.domain.actuator import Actuator as DomainActuator
from wadas.domain.camera import Camera as DomainCamera

Base = declarative_base()


# Classes
class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(SqlEnum(DomainCamera.CameraTypes), nullable=False)
    name = Column(String, nullable=True)
    enabled = Column(Boolean, default=False)
    actuators = relationship("Actuator", back_populates="camera")
    en_wadas_motion_detection = Column(Boolean, default=False)  # USBCamera specific
    pid = Column(String, nullable=True)  # USBCamera specific
    vid = Column(String, nullable=True)  # USBCamera specific
    path = Column(Text, nullable=True)  # USBCamera specific

    __mapper_args__ = {"polymorphic_identity": "camera", "polymorphic_on": type}


class USBCamera(Camera):
    __mapper_args__ = {"polymorphic_identity": DomainCamera.CameraTypes.USB_CAMERA.value}


class FTPCamera(Camera):
    __mapper_args__ = {"polymorphic_identity": DomainCamera.CameraTypes.FTP_CAMERA.value}


class Actuator(Base):
    __tablename__ = "actuators"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(SqlEnum(DomainActuator.ActuatorTypes), nullable=False)
    enabled = Column(Boolean, default=False)
    last_update = Column(Text, nullable=True)  # To handle date type
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=True)  # Relationship with Camera

    camera = relationship("Camera", back_populates="actuators")

    __mapper_args__ = {
        "polymorphic_identity": "actuator",
        "polymorphic_on": type,
    }


class RoadSignActuator(Actuator):
    __mapper_args__ = {
        "polymorphic_identity": DomainActuator.ActuatorTypes.ROADSIGN.value,
    }


class FeederActuator(Actuator):
    __mapper_args__ = {
        "polymorphic_identity": DomainActuator.ActuatorTypes.FEEDER.value,
    }


class DetectionEvent(Base):
    __tablename__ = "detection_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    camera_id = Column(String, nullable=False, index=True)
    time_stamp = Column(DateTime(timezone=True), nullable=False)
    original_image = Column(Text, nullable=False)
    detection_img_path = Column(Text, nullable=False)
    detected_animals = Column(Text, nullable=False)  # Use JSON if supported
    classification = Column(Boolean, default=True)
    classification_img_path = Column(Text, nullable=True)
    classified_animals = Column(Text, nullable=True)  # Use JSON if supported

    actuation_events = relationship(
        "ActuationEvent", back_populates="detection_event", cascade="all, delete-orphan"
    )


class ActuationEvent(Base):
    __tablename__ = "actuation_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    actuator_id = Column(String, nullable=False, index=True)
    time_stamp = Column(DateTime(timezone=True), nullable=False)
    detection_event_id = Column(Integer, ForeignKey("detection_events.id"), nullable=False)
    command = Column(Text, nullable=True)  # Use JSON if needed

    detection_event = relationship("DetectionEvent", back_populates="actuation_events")


# Database service tables, not mapped with any WADAS class
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)


class DBMetadata(Base):
    __tablename__ = "db_metadata"

    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(String, nullable=False, default=lambda: __dbversion__)
    applied_at = Column(DateTime(timezone=True), nullable=False)
    description = Column(Text, nullable=True)


# Indexes
Index("ix_detection_events_camera_time", DetectionEvent.camera_id, DetectionEvent.time_stamp)
Index("ix_actuation_events_actuator_time", ActuationEvent.actuator_id, ActuationEvent.time_stamp)
