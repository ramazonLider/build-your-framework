import pytest
from app import SimpleFrame
import wsgiadapter
import requests


@pytest.fixture
def app():
    return SimpleFrame()

@pytest.fixture
def test_client(app):
    return app.test_session()