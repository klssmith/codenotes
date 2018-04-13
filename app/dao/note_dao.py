from app.models import Note


def dao_get_all_notes():
    return Note.query.order_by(Note.title).all()
