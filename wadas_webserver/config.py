import os

SECRET_KEY = "your_secret_key"
REFRESH_SECRET_KEY = "your_refresh_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
CERT_FOLDER = os.path.join(CURRENT_DIRECTORY, "web_cert")
CERT_FILEPATH = os.path.join(CERT_FOLDER, "cert.pem")
KEY_FILEPATH = os.path.join(CERT_FOLDER, "key.pem")
