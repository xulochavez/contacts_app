import string
import random
import datetime

from contacts import celery, create_app
from contacts.db import Contact, Email, db, save_contact, purge_old_contacts


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
    save_contact(username=username, name=name, surname=surname, emails=emails)
    older_than_timestamp = datetime.datetime.now() - datetime.timedelta(seconds=60)
    purge_old_contacts(older_than_timestamp)
