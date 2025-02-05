import pytest
from fastapi.testclient import TestClient
from contextlib import contextmanager
from datetime import datetime
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    
@pytest.fixture
def mock_db_time():
    return _mock_db_time

@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 2, 5)):
    
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
            
    even.listen(model, 'before_insert', fake_time_hook)
    
    yield time
    
    event.remove(model, 'before_insert', fake_time_hook)
    
