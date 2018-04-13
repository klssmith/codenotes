from bs4 import BeautifulSoup
from flask import url_for

from app import db
from app.models import Note


def test_all_notes_appear_on_the_notes_page(client, codenotes_db_session):
    note_1 = Note(title='Ruby Notes', content='Some Ruby stuff')
    note_2 = Note(title='Python Notes', content='Some Python stuff')

    db.session.add_all([note_1, note_2])
    db.session.commit()

    response = client.get(url_for('notes.get_all_notes'))
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    assert 'Python Notes' in page.find_all('p')[0].string
    assert 'Ruby Notes' in page.find_all('p')[1].string
