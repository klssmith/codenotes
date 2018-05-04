from app.models import Note


def dao_get_note(note_id):
    return Note.query.get_or_404(note_id)


def dao_get_all_notes():
    return Note.query.order_by(Note.title).all()
