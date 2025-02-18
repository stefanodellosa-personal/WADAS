import os
from datetime import datetime

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from wadas.domain.db_model import Base
from wadas_webserver.database import Database
from wadas_webserver.view_model import Camera, DetectionEvent


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


def test_get_detection_events(database):
    count, detection_events = database.get_all_detection_events()
    assert len(detection_events) == count
    assert isinstance(detection_events[0], DetectionEvent)


def test_get_detection_events_by_camera_id(database):
    count, detection_events = database.get_detection_events_by_filter(camera_ids=[1])
    assert len(detection_events) > 0
    assert isinstance(detection_events[0], DetectionEvent)
    assert all(event.camera_id == 1 for event in detection_events)


def test_get_detection_events_by_date(database):
    datefrom = datetime(2025, 1, 19)
    dateto = datetime(2025, 1, 21)
    count, detection_events = database.get_detection_events_by_filter(
        date_from=datefrom, date_to=dateto
    )
    assert len(detection_events) > 0
    assert isinstance(detection_events[0], DetectionEvent)
    assert all(datefrom <= event.timestamp <= dateto for event in detection_events)
