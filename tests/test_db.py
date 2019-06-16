from datetime import datetime, timedelta
import pytest
from unittest import mock

from contacts import create_app
from contacts.config import TestConfig
from contacts.db import db, Contact, save_contact, load_contacts, purge_old_contacts


@pytest.fixture
def test_app():
    app = create_app(test_config=TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


def test_save_contact(test_app):
    with test_app.app_context():
        save_contact(username='mastershifu', name='master', surname='shifu', emails=['mshifu@kp.com','mshifu2@kp.com'])
        actual = Contact.query.all()

        assert len(actual) == 1
        assert actual[0].username == 'mastershifu'
        assert actual[0].name == 'master'
        assert actual[0].surname == 'shifu'
        assert [e.email for e in actual[0].emails] == ['mshifu@kp.com', 'mshifu2@kp.com']


def test_load_contacts(test_app):
    with test_app.app_context():
        save_contact(username='vpr', name='v', surname='viper', emails=['vpr@kp.com'])
        save_contact(username='mts', name='m', surname='mantis', emails=['mts@kp.com'])
        contacts = load_contacts()
        assert len(contacts) == 2
        assert dict(username='vpr', name='v', surname='viper', emails=['vpr@kp.com']) in contacts


def test_purge_old_contacts(test_app):
    with test_app.app_context():
        save_contact(username='vpr', name='v', surname='viper', emails=['vpr@kp.com'])

        # save contact as if it was saved 2 mins ago
        with mock.patch('contacts.db.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime.now() - timedelta(seconds=120)
            save_contact(username='mts', name='m', surname='mantis', emails=['mts@kp.com'])

        older_than_timestamp = datetime.now() - timedelta(seconds=60)
        purge_old_contacts(older_than_timestamp)

        contacts = load_contacts()
        assert len(contacts) == 1
        assert dict(username='vpr', name='v', surname='viper', emails=['vpr@kp.com']) in contacts





