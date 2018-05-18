from .forms import NoteForm

from flask import Blueprint, flash, redirect, render_template, url_for

from app import db
from app.dao.note_dao import dao_create_note, dao_get_all_notes, dao_get_note, dao_update_note


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
        flash('Your note was created successfully', 'success')
        return redirect(url_for('notes.get_one_note', note_id=note.id))

    return render_template('notes/new_note.html', form=form)


@notes.route('<uuid:note_id>/edit', methods=['GET', 'POST'])
def edit_note(note_id):
    note = dao_get_note(note_id)
    form = NoteForm(obj=note)

    if form.validate_on_submit():
        # note.title = form.title.data.strip()
        # note.content = form.content.data.strip()

        form.populate_obj(note)
    db.session.commit()

    return render_template('notes/edit_note.html', note=note, form=form)
