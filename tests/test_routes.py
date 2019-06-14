import pytest
import datetime
from unittest import mock

from contacts import create_app
from contacts.config import TestConfig
from contacts.db import db, Contact, load_contacts


@pytest.fixture
def test_client_with_populated_db():
    app = create_app(test_config=TestConfig)
    with app.app_context():
        db.create_all()

        db.session.add(Contact(username='mastershifu', name='master', surname='shifu', email='msf@kp.com'))
        db.session.add(Contact(username='mantis', name='m', surname='antis', email='mts@kp.com'))
        db.session.commit()

        client = app.test_client()
        yield client
        db.drop_all()


def test_get_contacts(test_client_with_populated_db):
    response = test_client_with_populated_db.get('/contacts_app/contacts')
    expected = [{'email': 'msf@kp.com', 'name': 'master', 'surname': 'shifu', 'username': 'mastershifu'},
                {'email': 'mts@kp.com', 'name': 'm', 'surname': 'antis', 'username': 'mantis'}]
    actual = response.json
    assert expected == actual


def test_get_contact(test_client_with_populated_db):
    response = test_client_with_populated_db.get('/contacts_app/contacts/mastershifu')
    expected = [{'email': 'msf@kp.com', 'name': 'master', 'surname': 'shifu', 'username': 'mastershifu'}]
    actual = response.json
    assert expected == actual


def test_add_contact(test_client_with_populated_db):
    response = test_client_with_populated_db.post('/contacts_app/contacts',
                           data='{"email": "vpr@kp.com", "name": "v", "surname": "viper", "username": "viper"}',
                           content_type='application/json')
    actual = response.json
    expected = [{'email': 'msf@kp.com', 'name': 'master', 'surname': 'shifu', 'username': 'mastershifu'},
                {'email': 'mts@kp.com', 'name': 'm', 'surname': 'antis', 'username': 'mantis'},
                {'email': 'vpr@kp.com', 'name': 'v', 'surname': 'viper', 'username': 'viper'}]
    assert expected == actual
    assert response.status_code == 201


def test_update_contact(test_client_with_populated_db):
    response = test_client_with_populated_db.put('/contacts_app/contacts/mastershifu',
                           data='{"email": "mshifu@kp.com", "name": "m"}',
                           content_type='application/json')
    actual = response.json
    expected = {'email': 'mshifu@kp.com', 'name': 'm', 'surname': 'shifu', 'username': 'mastershifu'}
    assert expected == actual
    assert response.status_code == 200


def test_delete_contact(test_client_with_populated_db):
    response = test_client_with_populated_db.delete('/contacts_app/contacts/mastershifu')
    assert response.status_code == 204
    expected_remaining_contacts = [{'username': 'mantis', 'email': 'mts@kp.com', 'name': 'm', 'surname': 'antis'}]
    contacts = load_contacts()
    assert expected_remaining_contacts == contacts



