from flask import Blueprint, render_template

from app.dao.note_dao import dao_get_all_notes, dao_get_note


notes = Blueprint('notes', __name__)


@notes.route('<uuid:note_id>')
def get_one_note(note_id):
    note = dao_get_note(note_id)
    return render_template('notes/one_note.html', note=note)


@notes.route('/')
def get_all_notes():
    notes = dao_get_all_notes()
    return render_template('notes/all_notes.html', notes=notes)
