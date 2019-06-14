# INSTRUCTIONS

# clone to a local folder

git clone git@github.com:xulochavez/contacts.git

# This will create contacts folder

# cd into contacts folder

# create virtualenv

# install requirements
pip install -r requirements.txt

# install currency_converter package
pip install .

# initialise database
init_db.sh

# run flask server
run.sh

# example query with curl
curl -i "http://localhost:5000/contacts_app/contacts"
curl -i -H "Content-Type: application/json" -X POST "http://localhost:5000/contacts_app/contacts" -d '{"username":"mastershifu", "name":"master", "surname":"shifu", "email":"mshifu@kp.com"}'
curl -i -H "Content-Type: application/json" -X PUT "http://localhost:5000/contacts_app/contacts/mastershifu" -d '{"surname":"shifuuu", "email":"mshifu_2@kp.com"}'

