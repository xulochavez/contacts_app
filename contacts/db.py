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
    username = db.Column(db.String(50), unique=1)
    email = db.Column(db.String(50))
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))

    def __repr__(self):
        return f'<Contact username: {self.username}, name:{self.name},  surname: {self.surname}, email: {self.email}>'

    def as_dict(self):
        "returns a dictionary of columns and values for the instance"
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in ['id']}

    @classmethod
    def get_cols(cls):
        return [c.name for c in cls.__table__.columns if c.name not in ['id']]


def save_contact(username, name, surname, email):
    new_contact = Contact(username=username, name=name, surname=surname, email=email)
    db.session.add(new_contact)
    db.session.commit()


def load_contacts(username=None):
    if username:
        contacts = Contact.query.filter(Contact.username == username).all()
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

    def update_attr(contact, col):
        if col in update_values and not isinstance(update_values[col], str):
            raise BadRequestError(400)
        setattr(contact, col, update_values.get(col, getattr(contact, col)))

    for col in Contact.get_cols():
        update_attr(contact, col)

    db.session.commit()

    return contact.as_dict()


def delete_db_contact(username):
    contacts = Contact.query.filter(Contact.username == username).all()
    if not contacts:
        raise NotFoundError(f"username {username} not found in db")

    contact = contacts[0]

    db.session.delete(contact)
    db.session.commit()







