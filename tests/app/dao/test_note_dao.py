import pytest
from sqlalchemy.exc import IntegrityError

from app import db
from app.dao.note_dao import dao_create_note, dao_get_all_notes, dao_get_note
from app.models import Note


def test_dao_get_all_notes_returns_all_notes_ordered_by_title(codenotes_db_session):
    note_1 = Note(title='Zebra', content='Some stuff')
    note_2 = Note(title='Apple', content='More stuff')

    db.session.add_all([note_1, note_2])
    db.session.commit()

    result = dao_get_all_notes()

    assert len(result) == 2
    assert result[0].title == 'Apple'
    assert result[1].title == 'Zebra'


def test_create_note_creates_new_note_if_valid(codenotes_db_session):
    created_note = dao_create_note('My title', 'My content')

    note = dao_get_note(created_note.id)

    assert note.title == 'My title'
    assert note.content == 'My content'
    assert note.created_at
    assert not note.updated_at


@pytest.mark.parametrize('title,content', [
    (None, 'My content'),
    ('My title', None),
])
def test_create_note_creates_new_note_raises_error_if_invalid(codenotes_db_session, title, content):
    with pytest.raises(IntegrityError):
        dao_create_note(title, content)
