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

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class DetectionEvent(Base):
    __tablename__ = "detection_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    camera_id = Column(String, nullable=False)
    time_stamp = Column(DateTime, nullable=False)
    original_image = Column(Text, nullable=False)
    detection_img_path = Column(Text, nullable=False)
    detected_animals = Column(Text, nullable=False)  # Serialized list (e.g., JSON)
    classification = Column(Boolean, default=True)
    classification_img_path = Column(Text, nullable=True)
    classified_animals = Column(Text, nullable=True)  # Serialized list (e.g., JSON)

    actuation_events = relationship("ActuationEvent", back_populates="detection_event")


class ActuationEvent(Base):
    __tablename__ = "actuation_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    actuator_id = Column(String, nullable=False)
    time_stamp = Column(DateTime, nullable=False)
    detection_event_id = Column(Integer, ForeignKey("detection_events.id"), nullable=False)
    command = Column(Text, nullable=True)

    detection_event = relationship("DetectionEvent", back_populates="actuation_events")
