from mock import MagicMock
from app.core.translator import Translator
from app.web import start_controllers
from flask.app import Flask
from injector import Injector
import pytest
from tests.factories import UserFactory
from app.models.entities import User
from app.injector import injector as injector_object
from tests.clear_collections import ClearCollections

start_controllers()


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def injector() -> Injector:
    return injector_object


@pytest.fixture
def translator(injector) -> Translator:
    return injector.get(Translator)


@pytest.fixture
def clear_collections(injector) -> ClearCollections:
    return injector.get(ClearCollections)


@pytest.fixture
def client():
    app = injector_object.get(Flask)
    with app.test_client() as client:
        with app.app_context():
            pass
        yield client


@pytest.fixture
def update():
    return MagicMock()


@pytest.fixture
def context():
    return MagicMock()
