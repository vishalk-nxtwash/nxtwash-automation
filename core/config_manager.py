import os

import yaml


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

    def __init__(self, env="staging"):

        self.load_dotenv()

        # Load environment-specific settings.
        with open(f"config/{env}.yaml") as file:
            self.config = yaml.safe_load(file)

    def load_dotenv(self, path=".env"):
        if not os.path.exists(path):
            return

        with open(path) as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#") or "=" not in line:
                    continue

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")

                if not value:
                    continue

                os.environ.setdefault(key, value)

    def get_url(self, portal):
        # Get the URL for the staging.
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
