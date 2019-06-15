from flask import Flask, make_response, jsonify
from flask_migrate import Migrate


from contacts.config import Config
from contacts import db, routes


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.from_object(test_config)
    else:
        app.config.from_object(Config)

    app.logger.info(f"connecting to db {app.config['SQLALCHEMY_DATABASE_URI']}")

    db.init_app(app)
    migrate = Migrate(app, db.db)

    app.register_blueprint(routes.bp)

    @app.errorhandler(500)
    def internal_server_error(error):
        return make_response(jsonify({'error': 'Internal Server error'}), 500)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    return app