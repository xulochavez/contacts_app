export FLASK_APP=contacts
export FLASK_ENV=development
flask db init
flask db migrate
flask db upgrade