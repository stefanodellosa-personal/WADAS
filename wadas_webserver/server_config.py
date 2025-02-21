import logging
import secrets
from pathlib import Path

import keyring

logger = logging.getLogger(__name__)


class ServerConfig:
    JWT_ENC_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    REFRESH_TOKEN_EXPIRE_DAYS = 7

    CURRENT_DIRECTORY = Path(__file__).resolve().parent
    CERT_FOLDER = CURRENT_DIRECTORY / "web_cert"
    CERT_FILEPATH = CERT_FOLDER / "cert.pem"
    KEY_FILEPATH = CERT_FOLDER / "key.pem"

    WADAS_ROOT_DIR = CURRENT_DIRECTORY / "../"

    instance = None

    def __init__(self, project_uuid):
        self.project_uuid = project_uuid

    def _get_or_set_secret_key(self, key_type):
        service_name = f"WADAS_web_server_{key_type}_{self.project_uuid}"
        username = f"{key_type}_token"

        if cred := keyring.get_credential(service_name, username):
            return cred.password

        secret = secrets.token_hex(32)
        keyring.set_password(service_name, username, secret)
        return secret

    @property
    def access_secret_key(self):
        return self._get_or_set_secret_key("access")

    @property
    def refresh_secret_key(self):
        return self._get_or_set_secret_key("refresh")
