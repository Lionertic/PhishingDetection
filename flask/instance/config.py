import os

user = os.environ['DB_USERNAME']
password = os.environ['DB_PASSWORD']
host = os.environ['DB_HOST']
database = os.environ['DB_DATABASE']
port = os.environ['DB_PORT']

# SECRET_KEY = 'p9Bv<3Eid9%$i01'
SQLALCHEMY_DATABASE_URI = 'mysql://' + user + ":" + password + "@" + host + ":" + port + "/" + database