from app import db
from app.dao.note_dao import dao_get_all_notes
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
