# INSTRUCTIONS

# for PART 1 checkout tag part1
# for PART 2 checkout tag part2

# clone to a local folder

git clone git@github.com:xulochavez/contacts_app.git

# This will create contacts_app folder

# cd into contacts_app folder

# create virtualenv

# install requirements
pip install -r requirements.txt

# install currency_converter package
pip install .

# run the tests
pytest tests

# initialise database
init_db.sh

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
