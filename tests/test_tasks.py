import pytest

from contacts import create_app
from contacts.config import TestConfig
from contacts.db import db, Contact, save_contact, load_contacts
from contacts.tasks import add_random_contacts


@pytest.fixture
def test_app():
    app = create_app(test_config=TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


def test_add_random_contacts(test_app):
    with test_app.app_context():
        add_random_contacts()

    actual = load_contacts()
    print(actual)
    assert len(actual) == 1
    assert len(actual[0]['name']) == 5
    assert actual[0]['username'] == actual[0]['name'] + actual[0]['surname']
