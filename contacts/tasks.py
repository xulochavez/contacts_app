import string
import random

from contacts import celery, create_app
from contacts.db import Contact, Email, db


def generate_randon_contact_details():
    name = ''.join(random.choices(string.ascii_letters, k=5))
    surname = ''.join(random.choices(string.ascii_letters, k=5))
    username = name + surname
    email1 = name + '@mail.com'
    email2 = name + '2@mail.com'
    return username, name, surname, [email1, email2]


@celery.task
def add_random_contacts():
    username, name, surname, emails = generate_randon_contact_details()
    new_contact = Contact(username=username, name=name, surname=surname,
                          emails=[Email(email=e) for e in emails])
    db.session.add(new_contact)
    db.session.commit()
    print(f"added {new_contact}")
