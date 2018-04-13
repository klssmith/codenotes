from flask import Blueprint, render_template

from app.dao.note_dao import dao_get_all_notes


notes = Blueprint('notes', __name__)


@notes.route('/')
def get_all_notes():
    notes = dao_get_all_notes()
    return render_template('notes/all_notes.html', notes=notes)
