from bs4 import BeautifulSoup
from flask import url_for

from app.dao.note_dao import dao_create_note


def test_all_notes_appear_on_the_notes_page_with_links(client, codenotes_db_session):
    note_1 = dao_create_note(title='Ruby Notes', content='Some Ruby stuff')
    note_2 = dao_create_note(title='Python Notes', content='Some Python stuff')

    response = client.get(url_for('notes.get_all_notes'))
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    note_one_link = page.find('a', string='Ruby Notes')
    note_two_link = page.find('a', string='Python Notes')

    assert note_one_link['href'] == '/notes/{}'.format(note_1.id)
    assert note_two_link['href'] == '/notes/{}'.format(note_2.id)


def test_get_one_note_displays_the_title_and_content(client, codenotes_db_session):
    note = dao_create_note(title='Ruby Notes', content='Some Ruby stuff')

    response = client.get(url_for('notes.get_one_note', note_id=note.id))
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    assert page.find('h1').string == 'Ruby Notes'
    assert page.find('div', class_='content').string.strip() == 'Some Ruby stuff'


def test_get_one_note_with_an_invalid_uuid_returns_404(client, codenotes_db_session):
    fake_uuid = '2c24f6d2-ddaf-42b7-a9e7-c09b017fa0ac'
    response = client.get(url_for('notes.get_one_note', note_id=fake_uuid))

    assert response.status_code == 404


def test_create_a_note_shows_new_note_page_with_valid_data(client, codenotes_db_session):
    title = 'My title'
    content = 'My content'

    response = client.post(
        url_for('notes.create_a_note'),
        data={'title': title, 'content': content},
        follow_redirects=True
    )
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    assert response.status_code == 200
    assert page.find('h1').string == title
    assert page.find('div', class_='content').string.strip() == content
    assert page.find('div', class_='alert alert-success').string.strip() == 'Your note was created successfully'


def test_create_a_note_strips_whitespace(client, codenotes_db_session):
    title = '         My title     '
    content = '          My content         '

    response = client.post(
        url_for('notes.create_a_note'),
        data={'title': title, 'content': content},
        follow_redirects=True
    )
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    assert response.status_code == 200
    assert page.find('h1').string == 'My title'
    assert page.find('div', class_='content').string == '\nMy content\n'


def test_create_a_note_with_invalid_fields_shows_errors_and_does_not_redirect(client):
    title = 'A title that is too far over the one hundred and twenty character limit, and so will cause validation \
    on the title length to fail.'
    content = ''

    response = client.post(
        url_for('notes.create_a_note'),
        data={'title': title, 'content': content},
    )
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    assert response.status_code == 200
    assert page.find('h1').string == 'Create a new note'
    assert len(page.find_all('div', class_='alert')) == 2
