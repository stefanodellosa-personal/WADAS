import logging

import pytest
from sqlalchemy import func, select

from wadas._version import __dbversion__
from wadas.domain.database import DataBase, SQLiteDataBase
from wadas.domain.db_model import (
    ActuationEvent,
    Actuator,
    Camera,
    ClassifiedAnimals,
    DBMetadata,
    DetectionEvent,
    FeederActuator,
    FTPCamera,
    RoadSignActuator,
    USBCamera,
    camera_actuator_association,
)

logger = logging.getLogger(__name__)


@pytest.fixture
def init():
    if DataBase.wadas_db_engine is not None:
        DataBase.destroy_instance()
        assert DataBase.wadas_db_engine is None
        assert DataBase.wadas_db is None
    if DataBase.wadas_db is not None:
        logger.debug("Found an active db instance before test execution...")
        DataBase.wadas_db = None


@pytest.fixture()
def db(init):
    assert DataBase.initialize(DataBase.DBTypes.SQLITE, ":memory:", None, "", "") is True
    db = DataBase.get_instance()
    session = DataBase.create_session()
    assert db.create_database() is True
    yield db, session
    DataBase.destroy_instance()


def test_database_already_created(init):
    DataBase.wadas_db = True
    with pytest.raises(RuntimeError, match="Database instance already created."):
        SQLiteDataBase("NOT-USED-HOST")


def test_database_already_initialized(init):
    DataBase.wadas_db = True
    assert DataBase.initialize(DataBase.DBTypes.SQLITE, "NOT-USED-HOST", None, "", "") is False


def test_no_host(init):
    assert DataBase.initialize(DataBase.DBTypes.SQLITE, "", None, "", "") is False


def test_unsupported_database(init):
    with pytest.raises(ValueError, match="Unsupported database type: DUMMY-DB-TYPE"):
        DataBase.initialize("DUMMY-DB-TYPE", "NOT-USED-HOST", None, "", "")


def test_no_engine_and_no_database(init):
    with pytest.raises(RuntimeError, match="The database and db engine have not been initialized."):
        SQLiteDataBase.get_engine()


def test_no_database(init):
    assert SQLiteDataBase.get_instance() is None


def test_failing_on_destroy_instance(init):
    DataBase.wadas_db_engine = True
    SQLiteDataBase.destroy_instance()
    assert DataBase.wadas_db_engine is None


def test_connection_string(db):
    db, session = db
    assert db is not None
    assert DataBase.wadas_db_engine is not None
    assert db.get_connection_string() == "sqlite:///:memory:"


def test_database_not_initialized(init):
    assert SQLiteDataBase("NOT-USED-HOST").create_database() is False


def test_serialize(init):
    assert SQLiteDataBase("NOT-USED-HOST").serialize() == {
        "host": "NOT-USED-HOST",
        "type": DataBase.DBTypes.SQLITE.value,
        "enabled": True,
        "version": __dbversion__,
    }
    assert SQLiteDataBase("NOT-USED-HOST2", False, "vX.Y.Z").serialize() == {
        "host": "NOT-USED-HOST2",
        "type": DataBase.DBTypes.SQLITE.value,
        "enabled": False,
        "version": "vX.Y.Z",
    }


def test_empty_database(db):
    db, session = db
    assert session.execute(select(func.count()).select_from(ActuationEvent)).scalar() == 0
    assert session.execute(select(func.count()).select_from(Actuator)).scalar() == 0
    assert session.execute(select(func.count()).select_from(Camera)).scalar() == 0
    assert session.execute(select(func.count()).select_from(ClassifiedAnimals)).scalar() == 0
    assert session.execute(select(func.count()).select_from(DBMetadata)).scalar() == 0
    assert session.execute(select(func.count()).select_from(DetectionEvent)).scalar() == 0
    assert session.execute(select(func.count()).select_from(FeederActuator)).scalar() == 0
    assert session.execute(select(func.count()).select_from(FTPCamera)).scalar() == 0
    assert session.execute(select(func.count()).select_from(RoadSignActuator)).scalar() == 0
    assert session.execute(select(func.count()).select_from(USBCamera)).scalar() == 0
    assert (
        session.execute(select(func.count()).select_from(camera_actuator_association)).scalar() == 0
    )
