import json

class ConfigLoader:
    def __init__(self, config_file: str):
        """
        Initializes the ConfigLoader with the configuration file path.
        """
        self.config_file = config_file

    def load_config(self):
        """
        Loads the configuration from the JSON file.
        """
        with open(self.config_file, "r") as file:
            config = json.load(file)
        return config

    def get_playlist_title(self) -> str:
        """
        Returns the playlist title from the configuration file.
        """
        config = self.load_config()
        return config["playlist_title"]

    def get_client_id(self) -> str:
        """
        Returns the client ID from the configuration file.
        """
        config = self.load_config()
        return config["client_id"]

    def get_client_secret(self) -> str:
        """
        Returns the client secret from the configuration file.
        """
        config = self.load_config()
        return config["client_secret"]
    
    def get_redirect_uri(self) -> str:
        config = self.load_config()
        return config["redirect_uri"]
