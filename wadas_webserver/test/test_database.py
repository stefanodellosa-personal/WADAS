import csv
import io
import os
from datetime import datetime

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from wadas.domain.db_model import Base
from wadas_webserver.database import Database
from wadas_webserver.view_model import (
    ActuationEvent,
    ActuationsRequest,
    Camera,
    DetectionEvent,
    DetectionsRequest,
)


def populate_fake_db(engine):
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    current_directory = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_directory, "test_data.txt")) as fin:
        for line in fin:
            line = line.strip()
            if line and not line.startswith("#"):
                session.execute(text(line.strip()))
    session.commit()
    session.close()


@pytest.fixture
def database():
    engine = create_engine("sqlite:///:memory:", echo=True)
    populate_fake_db(engine)
    db = Database("sqlite:///:memory:")
    db.engine = engine
    return db


def test_constructor(database):
    assert database is not None
    assert database.get_connection_string() == "sqlite:///:memory:"


def test_get_cameras(database):
    cameras = database.get_cameras()
    assert len(cameras) > 0
    assert isinstance(cameras[0], Camera)


def test_get_known_animals(database):
    known_animals = database.get_known_animals()
    assert len(known_animals) > 0
    assert isinstance(known_animals[0], str)


def test_get_known_actuators_types(database):
    actuators_types = database.get_known_actuator_types()
    assert len(actuators_types) > 0
    assert isinstance(actuators_types[0], str)


def test_get_known_actuation_commands(database):
    known_commands = database.get_known_actuation_commands()
    assert len(known_commands) > 0
    assert isinstance(known_commands[0], str)


def test_get_detection_events(database):
    count, detection_events = database.get_all_detection_events()
    assert len(detection_events) == count
    assert isinstance(detection_events[0], DetectionEvent)


def test_get_detection_events_by_camera_id(database):
    camera_id = 7

    request = DetectionsRequest(camera_ids=[camera_id])
    count, detection_events = database.get_detection_events_by_filter(request)
    assert len(detection_events) > 0
    assert isinstance(detection_events[0], DetectionEvent)
    assert all(event.camera_id == camera_id for event in detection_events)


def test_get_detection_events_by_date(database):
    datefrom = datetime(2025, 2, 8)
    dateto = datetime(2025, 2, 15)

    request = DetectionsRequest(date_from=datefrom, date_to=dateto)
    count, detection_events = database.get_detection_events_by_filter(request)
    assert len(detection_events) > 0
    assert isinstance(detection_events[0], DetectionEvent)
    assert all(datefrom <= event.timestamp <= dateto for event in detection_events)


def test_get_detection_events_by_animal(database):
    animals = ["cat"]

    request = DetectionsRequest(classified_animals=animals)
    count, detection_events = database.get_detection_events_by_filter(request)
    assert len(detection_events) > 0
    assert isinstance(detection_events[0], DetectionEvent)
    assert all(
        any(animal.animal in animals for animal in event.classified_animals)
        for event in detection_events
    )


def test_get_detection_events_by_camera_animal_date(database):
    camera_id = 7
    animals = ["bear"]
    datefrom = datetime(2025, 2, 8)
    dateto = datetime(2025, 2, 15)

    request = DetectionsRequest(
        camera_ids=[camera_id], classified_animals=animals, date_from=datefrom, date_to=dateto
    )
    count, detection_events = database.get_detection_events_by_filter(request)
    assert len(detection_events) > 0
    assert all(
        (
            event.camera_id == camera_id
            and datefrom <= event.timestamp <= dateto
            and any(animal.animal in animals for animal in event.classified_animals)
            for event in detection_events
        )
    )


def test_get_actuation_events(database):
    request = ActuationsRequest(limit=1000)

    count, actuation_events = database.get_actuation_events_by_filter(request)
    assert len(actuation_events) == count
    assert isinstance(actuation_events[0], ActuationEvent)


def test_get_actuation_events_by_actuator_type(database):
    actuator_type = "Feeder"

    request = ActuationsRequest(actuator_types=[actuator_type])
    count, actuation_events = database.get_actuation_events_by_filter(request)
    assert len(actuation_events) > 0
    assert isinstance(actuation_events[0], ActuationEvent)
    assert all(event.actuator.type == actuator_type for event in actuation_events)


def test_get_actuation_events_by_command(database):
    command = "display"

    request = ActuationsRequest(commands=[command])
    count, actuation_events = database.get_actuation_events_by_filter(request)
    assert len(actuation_events) > 0
    assert isinstance(actuation_events[0], ActuationEvent)
    assert all(event.command == command for event in actuation_events)


def test_get_actuation_events_by_date(database):
    datefrom = datetime(2025, 2, 8)
    dateto = datetime(2025, 2, 15)

    request = ActuationsRequest(date_from=datefrom, date_to=dateto)
    count, actuation_events = database.get_actuation_events_by_filter(request)
    assert len(actuation_events) > 0
    assert isinstance(actuation_events[0], ActuationEvent)
    assert all(datefrom <= event.timestamp <= dateto for event in actuation_events)


def test_get_actuation_events_by_command_date(database):
    command = "display"
    datefrom = datetime(2025, 2, 8)
    dateto = datetime(2025, 2, 15)

    request = ActuationsRequest(commands=[command], date_from=datefrom, date_to=dateto)
    count, actuation_events = database.get_actuation_events_by_filter(request)
    assert len(actuation_events) > 0
    assert isinstance(actuation_events[0], ActuationEvent)
    assert all(
        datefrom <= event.timestamp <= dateto and event.command == command
        for event in actuation_events
    )


def validate_csv_string(csv_string, headers_number):
    assert isinstance(csv_string, str)

    csv_file = io.StringIO(csv_string)
    reader = csv.reader(csv_file)

    lines = list(reader)
    assert len(lines) > 0

    header = lines[0]
    assert len(header) == headers_number

    if len(lines) > 1:
        first_data_row = lines[1]
        assert len(first_data_row) == len(header)


def test_export_filtered_detection_events(database):
    camera_id = 7
    datefrom = datetime(2025, 2, 8)
    dateto = datetime(2025, 2, 15)

    request = DetectionsRequest(camera_ids=[camera_id], date_from=datefrom, date_to=dateto)
    csv_string = database.export_detection_events_as_csv(request)
    validate_csv_string(csv_string, 6)


def test_export_filtered_actuation_events(database):
    command = "display"
    datefrom = datetime(2025, 2, 8)
    dateto = datetime(2025, 2, 15)

    request = ActuationsRequest(commands=[command], date_from=datefrom, date_to=dateto)
    csv_string = database.export_actuation_events_as_csv(request)
    validate_csv_string(csv_string, 3)
