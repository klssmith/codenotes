from bs4 import BeautifulSoup
from flask import url_for

from app import db
from app.models import Note


def test_all_notes_appear_on_the_notes_page_with_links(client, codenotes_db_session):
    note_1 = Note(title='Ruby Notes', content='Some Ruby stuff')
    note_2 = Note(title='Python Notes', content='Some Python stuff')

    db.session.add_all([note_1, note_2])
    db.session.commit()

    response = client.get(url_for('notes.get_all_notes'))
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    note_one_link = page.find('a', string='Ruby Notes')
    note_two_link = page.find('a', string='Python Notes')

    assert note_one_link['href'] == '/notes/{}'.format(note_1.id)
    assert note_two_link['href'] == '/notes/{}'.format(note_2.id)


def test_get_one_note_displays_the_title_and_content(client, codenotes_db_session):
    note = Note(title='Ruby Notes', content='Some Ruby stuff')
    db.session.add(note)
    db.session.commit()

    response = client.get(url_for('notes.get_one_note', note_id=note.id))
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    assert page.find('h1').string == 'Ruby Notes'
    assert page.find('div').string.strip() == 'Some Ruby stuff'


def test_get_one_note_with_an_invalid_uuid_returns_404(client, codenotes_db_session):
    fake_uuid = '2c24f6d2-ddaf-42b7-a9e7-c09b017fa0ac'
    response = client.get(url_for('notes.get_one_note', note_id=fake_uuid))

    assert response.status_code == 404
