from .forms import NoteForm

from flask import Blueprint, redirect, render_template, url_for

from app.dao.note_dao import dao_create_note, dao_get_all_notes, dao_get_note


notes = Blueprint('notes', __name__)


@notes.route('<uuid:note_id>')
def get_one_note(note_id):
    note = dao_get_note(note_id)
    return render_template('notes/one_note.html', note=note)


@notes.route('/')
def get_all_notes():
    notes = dao_get_all_notes()
    return render_template('notes/all_notes.html', notes=notes)


@notes.route('/new', methods=['GET', 'POST'])
def create_a_note():
    form = NoteForm()

    if form.validate_on_submit():
        title = form.title.data.strip()
        content = form.content.data.strip()

        note = dao_create_note(title, content)
        return redirect(url_for('notes.get_one_note', note_id=note.id))

    return render_template('notes/new_note.html', form=form)
