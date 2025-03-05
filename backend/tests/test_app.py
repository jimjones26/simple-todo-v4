import pytest
from backend.app import create_app
from flask import Flask

def test_app_initialization():
    app = create_app()
    assert isinstance(app, Flask)
