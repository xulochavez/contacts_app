import click

from flask.cli import with_appcontext

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    db.create_all()
    click.echo('Initialized the database.')


def init_app(app):
    db.init_app(app)
    app.cli.add_command(init_db_command)


class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    emails = db.relationship('Email', backref=db.backref('contact', lazy=True), cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f'<Contact username: {self.username}, name:{self.name},  surname: {self.surname}, email: {self.email}>'

    def as_dict(self):
        "returns a dictionary of columns and values for the instance"
        as_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in ['id']}
        as_dict['emails'] = [e.email for e in self.emails]
        return as_dict

    @classmethod
    def get_cols(cls):
        return [c.name for c in cls.__table__.columns if c.name not in ['id']] + ['emails']


class Email(db.Model):
    __tablename__ = "emails"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id', ondelete='CASCADE'))

    def __repr__(self):
        return f'<Email email: {self.email}>'


def save_contact(username, name, surname, emails):
    new_contact = Contact(username=username, name=name, surname=surname)
    new_contact.emails.extend([Email(email=email) for email in emails])
    db.session.add(new_contact)
    db.session.commit()


def load_contacts(username=None, email=None):
    if username:
        contacts = Contact.query.filter(Contact.username == username).all()
    elif email:
        email_objs = Email.query.filter(Email.email == email).all()
        contacts = [e.contact for e in email_objs]
    else:
        contacts = Contact.query.all()

    return [c.as_dict() for c in contacts]


class NotFoundError(Exception):
    pass


class BadRequestError(Exception):
    pass


def update_db_contact(username, update_values):
    contacts = Contact.query.filter(Contact.username == username).all()
    if not contacts:
        raise NotFoundError(f"username {username} not found in db")

    contact = contacts[0]

    def update_emails():
        if not isinstance(update_values[col], list):
            raise BadRequestError(400)
        contact.emails = [Email(email=e) for e in update_values[col]]

    def update_standard_cols(col):
        if col in update_values and not isinstance(update_values[col], str):
            raise BadRequestError(400)
        setattr(contact, col, update_values.get(col, getattr(contact, col)))

    for col in Contact.get_cols():
        if col not in update_values:
            continue

        if col == 'emails':
            update_emails()
        else:
            update_standard_cols(col)

    db.session.commit()

    return contact.as_dict()


def delete_db_contact(username):
    contacts = Contact.query.filter(Contact.username == username).all()
    if not contacts:
        raise NotFoundError(f"username {username} not found in db")

    contact = contacts[0]

    db.session.delete(contact)
    db.session.commit()







