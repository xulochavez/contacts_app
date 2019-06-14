from flask import Blueprint, jsonify, request, abort
from contacts.db import (load_contacts, save_contact, update_db_contact, delete_db_contact,
                         Contact, NotFoundError, BadRequestError)

bp = Blueprint('app_routes', __name__, url_prefix='/contacts_app')


@bp.route("/")
def index():
    return "Welcome to the contacts app"


@bp.route('/contacts', methods=['GET'])
def get_contacts():
    return jsonify(load_contacts())


@bp.route('/contacts/<string:username>', methods=['GET'])
def get_contact(username):
    return jsonify(load_contacts(username=username))


@bp.route('/contacts', methods=['POST'])
def add_contact():
    columns = Contact.get_cols()
    if not request.json or any([col not in request.json for col in columns]):
        abort(400)
    contact_attrs = {col: request.json[col] for col in columns}

    save_contact(**contact_attrs)
    all_contacts = load_contacts()

    return jsonify(all_contacts), 201


@bp.route('/contacts/<string:username>', methods=['PUT'])
def update_contact(username):
    if not request.json:
        abort(400)

    try:
        contact = update_db_contact(username, request.json)
    except NotFoundError:
        abort(404)
    except BadRequestError:
        abort(400)

    return jsonify(contact), 200


@bp.route('/contacts/<string:username>', methods=['DELETE'])
def delete_contact(username):
    try:
        delete_db_contact(username)
    except NotFoundError:
        abort(404)

    return '', 204


