import yaml


class ConfigManager:

    def __init__(self, env="staging"):

        # Load environment-specific settings.
        with open(f"config/{env}.yaml") as file:
            self.config = yaml.safe_load(file)

        # Load user credentials.
        with open("config/users.yaml") as file:
            self.users = yaml.safe_load(file)

    def get_url(self, portal):
        # Get the URL for the staging.
        return self.config[portal]["url"]

    def get_username(self, portal):
        # Get the username for the ccc
        return self.users[portal]["username"]

    def get_password(self, portal):
        # Get the password for the staging.
        return self.users[portal]["password"]