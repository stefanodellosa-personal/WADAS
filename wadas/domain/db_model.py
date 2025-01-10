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
Base = declarative_base()


class Camera(Base):
    __tablename__ = "cameras"

    local_id = Column(Integer, primary_key=True, autoincrement=True)  # DB id
    camera_id = Column(String, nullable=False, unique=True)  # Unique external ID
    type = Column(SqlEnum(DomainCamera.CameraTypes), nullable=False)
    enabled = Column(Boolean, default=False)
    actuators = relationship("Actuator", back_populates="camera")
    detection_events = relationship(
        "DetectionEvent", back_populates="camera", cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "polymorphic_identity": "camera",
        "polymorphic_on": type,
    }


class USBCamera(Camera):
    __tablename__ = "usb_cameras"

    local_id = Column(Integer, ForeignKey("cameras.local_id"), primary_key=True)
    name = Column(String, nullable=True)
    en_wadas_motion_detection = Column(Boolean, default=False)
    pid = Column(String, nullable=True)
    vid = Column(String, nullable=True)
    path = Column(Text, nullable=True)

    __mapper_args__ = {"polymorphic_identity": DomainCamera.CameraTypes.USB_CAMERA}


class FTPCamera(Camera):
    __tablename__ = "ftp_cameras"

    local_id = Column(Integer, ForeignKey("cameras.local_id"), primary_key=True)
    ftp_folder = Column(Text, nullable=False)

    __mapper_args__ = {"polymorphic_identity": DomainCamera.CameraTypes.FTP_CAMERA}


class Actuator(Base):
    __tablename__ = "actuators"

    local_id = Column(Integer, primary_key=True, autoincrement=True)  # DB id and primary key
    actuator_id = Column(String, nullable=False, unique=True)  # DB unique identifier
    type = Column(SqlEnum(DomainActuator.ActuatorTypes), nullable=False)
    enabled = Column(Boolean, default=False)
    last_update = Column(Text, nullable=True)  # To handle date type
    camera_id = Column(
        Integer, ForeignKey("cameras.local_id"), nullable=True
    )  # Relationship with Camera

    camera = relationship("Camera", back_populates="actuators")
    actuation_events = relationship(
        "ActuationEvent", back_populates="actuator", cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "polymorphic_identity": "actuator",
        "polymorphic_on": type,
    }


class RoadSignActuator(Actuator):
    __mapper_args__ = {
        "polymorphic_identity": DomainActuator.ActuatorTypes.ROADSIGN,
    }


class FeederActuator(Actuator):
    __mapper_args__ = {
        "polymorphic_identity": DomainActuator.ActuatorTypes.FEEDER,
    }


class DetectionEvent(Base):
    __tablename__ = "detection_events"

    local_id = Column(Integer, primary_key=True, autoincrement=True)  # db ID
    camera_id = Column(Integer, ForeignKey("cameras.local_id"), nullable=False)
    time_stamp = Column(DateTime(timezone=True), nullable=False)
    original_image = Column(Text, nullable=False)
    detection_img_path = Column(Text, nullable=False)
    detected_animals = Column(Text, nullable=False)  # Use JSON if supported
    classification = Column(Boolean, default=True)
    classification_img_path = Column(Text, nullable=True)
    classified_animals = Column(Text, nullable=True)  # Use JSON if supported

    camera = relationship("Camera", back_populates="detection_events")
    actuation_events = relationship(
        "ActuationEvent", back_populates="detection_event", cascade="all, delete-orphan"
    )


class ActuationEvent(Base):
    __tablename__ = "actuation_events"

    local_id = Column(Integer, primary_key=True, autoincrement=True)  # db ID
    actuator_id = Column(Integer, ForeignKey("actuators.local_id"), nullable=False)
    time_stamp = Column(DateTime(timezone=True), nullable=False)
    detection_event_id = Column(Integer, ForeignKey("detection_events.local_id"), nullable=False)
    command = Column(Text, nullable=True)  # Use JSON if needed

    actuator = relationship("Actuator", back_populates="actuation_events")
    detection_event = relationship("DetectionEvent", back_populates="actuation_events")


# Database service tables, not mapped with any WADAS class
class User(Base):
    __tablename__ = "users"

    local_id = Column(String, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)


class DBMetadata(Base):
    __tablename__ = "db_metadata"

    local_id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(String, nullable=False, default=lambda: __dbversion__)
    applied_at = Column(DateTime(timezone=True), nullable=False)
    description = Column(Text, nullable=True)


# Indexes
Index("ix_detection_events_camera_time", DetectionEvent.camera_id, DetectionEvent.time_stamp)
Index("ix_actuation_events_actuator_time", ActuationEvent.actuator_id, ActuationEvent.time_stamp)
