import os

import yaml
from dotenv import load_dotenv


class ConfigManager:

    CREDENTIAL_ENV_VARS = {
        "superadmin": {
            "username": "SUPERADMIN_USERNAME",
            "password": "SUPERADMIN_PASSWORD"
        },
        "admin_portal": {
            "username": "ADMIN_PORTAL_USERNAME",
            "password": "ADMIN_PORTAL_PASSWORD"
        }
    }

    def __init__(self, env=None):

        load_dotenv(override=False)

        # Resolve the target environment: explicit arg > TEST_ENV > staging.
        if env is None:
            env = os.getenv("TEST_ENV", "staging")
        self.env = env

        # Load environment-specific settings.
        with open(f"config/{env}.yaml") as file:
            self.config = yaml.safe_load(file)

    def get_url(self, portal):
        return self.config[portal]["url"]

    def get_credential(self, portal, credential_type):
        env_var = self.CREDENTIAL_ENV_VARS[portal][credential_type]
        value = os.getenv(env_var)

        if not value:
            raise RuntimeError(
                "Missing required environment variable '%s' for %s %s."
                % (env_var, portal, credential_type)
            )

        return value

    def get_username(self, portal):
        # Get username from environment variables.
        return self.get_credential(portal, "username")

    def get_password(self, portal):
        # Get password from environment variables.
        return self.get_credential(portal, "password")
