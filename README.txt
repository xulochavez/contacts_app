# INSTRUCTIONS

# for PART 1 checkout tag part1
# for PART 2 checkout tag part2
# for PART 3 checkout tag part3

# clone to a local folder

git clone git@github.com:xulochavez/contacts_app.git

# This will create contacts_app folder

# cd into contacts_app folder

# create and activate virtualenv

# install requirements
pip install -r requirements.txt

# install currency_converter package
pip install .

# run the tests
pytest tests

### For part2 and part3 only
#
# delete existing sqlite db prod file  (from config: /tmp/contacts.db) (Tables have the old schema)
# and initialise database
init_db.sh

# (alternatively run migration using flask-migrate
# however this needs manual changes to the automatically generated file, see migrations/versions/bf766f555772_.py
# required commands are kept in scripts/migrate.sh)
#
### end of for part2 and part3 only

# run flask server
run.sh

# example queries with curl
# get all contacts
curl -i "http://localhost:5000/contacts_app/contacts"
# get contact for a given username
curl -i "http://localhost:5000/contacts_app/contact/mastershifu"
# get contact for a given email
curl -i "http://localhost:5000/contacts_app/contacts?email=mshifu@kp.com"
# create new contact
curl -i -H "Content-Type: application/json" -X POST "http://localhost:5000/contacts_app/contacts" -d '{"username":"mastershifu", "name":"master", "surname":"shifu", "email":["mshifu@kp.com"]}'
# update contact
curl -i -H "Content-Type: application/json" -X PUT "http://localhost:5000/contacts_app/contacts/mastershifu" -d '{"surname":"shifuuu", "email":["mshifu_2@kp.com"]}'
# delete contact
curl -i "http://localhost:5000/contacts_app/contact/mastershifu" -X DELETE

# part 3: periodic task with celery

# run the celery beat scheduler - from the project folder, contacts_app
celery -A celery_worker:celery beat --loglevel=info

# run the celery worker - in another terminal, from the project folder, contacts_app
celery -A celery_worker:celery worker--loglevel=info