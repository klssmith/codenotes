import pytest

from app.dao.note_dao import dao_create_note


@pytest.fixture
def note(codenotes_db_session):
    return dao_create_note(title='Testing code', content='All about writing tests.')
