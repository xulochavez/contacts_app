import pytest
import datetime
from unittest import mock

from contacts import create_app
from contacts.config import TestConfig
from contacts.db import db, Contact, Email, load_contacts


@pytest.fixture
def test_client_with_populated_db():
    app = create_app(test_config=TestConfig)
    with app.app_context():
        db.create_all()

        db.session.add(Contact(username='mastershifu', name='master', surname='shifu', emails=[Email(email='msf@kp.com')]))
        db.session.add(Contact(username='mantis', name='m', surname='antis', emails=[Email(email='mts@kp.com')]))
        db.session.commit()

        client = app.test_client()
        yield client
        db.drop_all()


def test_get_contacts(test_client_with_populated_db):
    response = test_client_with_populated_db.get('/contacts_app/contacts')
    expected = [{'emails': ['msf@kp.com'], 'name': 'master', 'surname': 'shifu', 'username': 'mastershifu'},
                {'emails': ['mts@kp.com'], 'name': 'm', 'surname': 'antis', 'username': 'mantis'}]
    actual = response.json
    assert expected == actual


def test_get_contact(test_client_with_populated_db):
    response = test_client_with_populated_db.get('/contacts_app/contacts/mastershifu')
    expected = {'emails': ['msf@kp.com'], 'name': 'master', 'surname': 'shifu', 'username': 'mastershifu'}
    actual = response.json
    assert expected == actual


def test_get_contact_by_email(test_client_with_populated_db):
    response = test_client_with_populated_db.get('/contacts_app/contacts?email=msf@kp.com')
    expected = [{'emails': ['msf@kp.com'], 'name': 'master', 'surname': 'shifu', 'username': 'mastershifu'}]
    actual = response.json
    assert expected == actual


def test_add_contact(test_client_with_populated_db):
    response = test_client_with_populated_db.post('/contacts_app/contacts',
                           data='{"emails": ["vpr@kp.com"], "name": "v", "surname": "viper", "username": "viper"}',
                           content_type='application/json')
    actual = response.json
    expected = [{'emails': ['msf@kp.com'], 'name': 'master', 'surname': 'shifu', 'username': 'mastershifu'},
                {'emails': ['mts@kp.com'], 'name': 'm', 'surname': 'antis', 'username': 'mantis'},
                {'emails': ['vpr@kp.com'], 'name': 'v', 'surname': 'viper', 'username': 'viper'}]
    assert response.status_code == 201
    assert expected == actual



def test_update_contact(test_client_with_populated_db):
    response = test_client_with_populated_db.put('/contacts_app/contacts/mastershifu',
                           data='{"emails": ["mshifu@kp.com"], "name": "m"}',
                           content_type='application/json')
    actual = response.json
    expected = {'emails': ['mshifu@kp.com'], 'name': 'm', 'surname': 'shifu', 'username': 'mastershifu'}
    assert response.status_code == 200
    assert expected == actual


def test_update_clear_contact_emails(test_client_with_populated_db):
    response = test_client_with_populated_db.put('/contacts_app/contacts/mastershifu',
                           data='{"emails": []}',
                           content_type='application/json')
    actual = response.json
    expected = {'emails': [], 'name': 'master', 'surname': 'shifu', 'username': 'mastershifu'}
    assert response.status_code == 200
    assert expected == actual


def test_delete_contact(test_client_with_populated_db):
    response = test_client_with_populated_db.delete('/contacts_app/contacts/mastershifu')
    assert response.status_code == 204
    expected_remaining_contacts = [{'username': 'mantis', 'emails': ['mts@kp.com'], 'name': 'm', 'surname': 'antis'}]
    contacts = load_contacts()
    assert expected_remaining_contacts == contacts


def test_delete_contact_deletes_associated_emails(test_client_with_populated_db):
    response = test_client_with_populated_db.delete('/contacts_app/contacts/mastershifu')
    assert response.status_code == 204
    emails = Email.query.all()
    assert ['mts@kp.com'] == [e.email for e in emails]



