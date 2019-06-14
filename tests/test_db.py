import datetime
import pytest

from contacts import create_app
from contacts.config import TestConfig
from contacts.db import db, Contact, save_contact, load_contacts


@pytest.fixture
def test_app():
    app = create_app(test_config=TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


def test_save_contact(test_app):
    with test_app.app_context():
        save_contact(username='mastershifu', name='master', surname='shifu', email='mshifu@kp.com')
        actual = Contact.query.all()

        assert len(actual) == 1
        assert actual[0].username == 'mastershifu'
        assert actual[0].name == 'master'
        assert actual[0].surname == 'shifu'
        assert actual[0].email == 'mshifu@kp.com'


def test_load_contacts(test_app):
    with test_app.app_context():
        save_contact(username='vpr', name='v', surname='viper', email='vpr@kp.com')
        save_contact(username='mts', name='m', surname='mantis', email='mts@kp.com')
        contacts = load_contacts()
        assert len(contacts) == 2
        assert dict(username='vpr', name='v', surname='viper', email='vpr@kp.com') in contacts






