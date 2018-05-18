from app import db
from app.models import Note
from app.notes.errors import NoteNotFound


def dao_get_note(note_id):
    return Note.query.get_or_404(note_id)


def dao_get_all_notes():
    return Note.query.order_by(Note.title).all()


def dao_create_note(title, content):
    note = Note(title=title, content=content)

    db.session.add(note)
    db.session.commit()
    return note


def dao_update_note(note):
    if not note.id:
        raise NoteNotFound('The Note you are trying to update does not exist')

    db.session.add(note)
    db.session.commit()

    return note
