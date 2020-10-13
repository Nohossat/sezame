import os

if "MONGO_USERNAME" in os.environ:
    mongo_local_user = os.environ["MONGO_USERNAME"]
else :
    mongo_local_user = "m103-admin"

if "MONGO_PWD" in os.environ:
    mongo_local_pwd = os.environ["MONGO_PWD"]
else :
    mongo_local_pwd = "m103-pass"

if "MONGO_HOST" in os.environ:
    mongo_localhost = os.environ["MONGO_HOST"]
else :
    mongo_localhost = "localhost"

mongo_local_port = "27017"
spotify_auth = "BQBWmNVK1ssR8K1obFKxxj6rcV85mAC8djWrUnDzfoOwk8RwFHCsqdPYKE1raUbQB72c-GroyQJKv1jH9PIXQX7lE1dn8hccCj8inZEEQX2YjyMyaIcvWLAkbNOwz5r-zOVy7QEDp7DvibpP73lgGRa-hHIWH4P6Eu8P0yBnwJD6mWAjUR0bNw"