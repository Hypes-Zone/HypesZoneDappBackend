import os
from typing import Any, Generator

import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine():
    return create_engine(
        os.getenv("ALCHEMY_DB_URL"), connect_args={"check_same_thread": False}
    )

def get_session():
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


os.environ["ALCHEMY_DB_URL"] = os.getenv("TEST_ALCHEMY_DB_URL", "sqlite:///test.db")
os.environ["SECRET_KEY"] = os.getenv("TEST_SECRET_KEY", "testsecret")


from db.connector import Base, get_db
from main import app


@pytest.fixture(autouse=True)
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(get_engine())  # Create the tables.
    _app = app
    yield _app
    Base.metadata.drop_all(get_engine())


@pytest.fixture
def db_session(app: FastAPI) -> Generator[get_session(), Any, None]:
    """
    Creates a fresh sqlalchemy session for each test that operates in a
    transaction. The transaction is rolled back at the end of each test ensuring
    a clean state.
    """
    engine = get_engine()
    Session = get_session()

    # connect to the database
    connection = engine.connect()
    # begin a non-ORM transaction
    transaction = connection.begin()
    # bind an individual Session to the connection
    session = Session(bind=connection)
    yield session  # use the session in tests.
    session.close()
    # rollback - everything that happened with the
    # Session above (including calls to commit())
    # is rolled back.
    transaction.rollback()
    # return connection to the Engine
    connection.close()


@pytest.fixture()
def client(app: FastAPI, db_session: get_session()) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
