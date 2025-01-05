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

from wadas.domain.actuator import Actuator
from wadas.domain.camera import Camera

Base = declarative_base()


class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(SqlEnum(Camera.CameraTypes), nullable=False)
    name = Column(String, nullable=True)
    enabled = Column(Boolean, default=False)
    actuators = relationship("Actuator", back_populates="camera")
    ftp_folder = Column(Text, nullable=True)  # FTPCamera specific
    index = Column(Integer, nullable=True)  # USBCamera specific
    backend = Column(Integer, nullable=True)  # USBCamera specific
    en_wadas_motion_detection = Column(Boolean, default=False)  # USBCamera specific
    pid = Column(String, nullable=True)  # USBCamera specific
    vid = Column(String, nullable=True)  # USBCamera specific
    path = Column(Text, nullable=True)  # USBCamera specific

    __mapper_args__ = {"polymorphic_identity": "camera", "polymorphic_on": type}


class USBCamera(Camera):
    __mapper_args__ = {"polymorphic_identity": Camera.CameraTypes.USB_CAMERA.value}


class FTPCamera(Camera):
    __mapper_args__ = {"polymorphic_identity": Camera.CameraTypes.FTP_CAMERA.value}


class Actuator(Base):
    __tablename__ = "actuators"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(SqlEnum(Actuator.ActuatorTypes), nullable=False)
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
        "polymorphic_identity": Actuator.ActuatorTypes.ROADSIGN.value,
    }


class FeederActuator(Actuator):
    __mapper_args__ = {
        "polymorphic_identity": Actuator.ActuatorTypes.FEEDER.value,
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


# Indexes
Index("ix_detection_events_camera_id", DetectionEvent.camera_id)
Index("ix_actuation_events_actuator_id", ActuationEvent.actuator_id)
