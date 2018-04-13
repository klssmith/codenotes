import os

from alembic.command import upgrade
from alembic.config import Config
import pytest

from app import create_app, db


@pytest.fixture(scope='session')
def test_app():
    app = create_app('test')

    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture
def client(test_app):
    with test_app.test_request_context(), test_app.test_client() as client:
        yield client


@pytest.fixture(scope='session')
def codenotes_db(test_app):
    assert 'codenotes_test' in db.engine.url.database, 'Only run tests against the test database'

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    ALEMBIC_CONFIG = os.path.join(BASE_DIR, 'migrations')
    config = Config(ALEMBIC_CONFIG + '/alembic.ini')
    config.set_main_option("script_location", ALEMBIC_CONFIG)

    upgrade(config, 'head')

    yield db

    db.session.remove()
    db.get_engine(test_app).dispose()


@pytest.fixture
def codenotes_db_session(codenotes_db):
    yield codenotes_db

    codenotes_db.session.remove()
    for tbl in reversed(codenotes_db.metadata.sorted_tables):
        codenotes_db.engine.execute(tbl.delete())
