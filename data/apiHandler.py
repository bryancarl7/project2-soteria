"""
apiKeyLoader.py
===============================================================================
Last Modified: 25 May 2020
Modification By: Bryan Carl
Creation Date: 22 May 2020
Initial Author: Bryan Carl
===============================================================================
"""
import configparser
import os


class apiKeyLoader:
    def __init__(self):
        self.config_file = "credentials.ini"
        self.api_key = ""
        self.setup_credentials()

    def setup_credentials(self):
        # Setup ConfigParser
        config = configparser.ConfigParser()

        # Cannot find credentials.ini file, raise error
        if not os.path.isfile("credentials.ini"):
            raise FileNotFoundError("credentials.ini")

        # Read that MF in
        config.read("credentials.ini")

        try:
            # Attempt to load API key
            self.api_key = config.get("DEFAULT", "GoogleMapsAPIKey")
        except Exception as ex:
            # Invalid credentials.ini
            print(ex.__traceback__)
            raise FileNotFoundError("Could not parse credentials.ini, make sure it is included")

    def get_api_key(self):
        return self.api_key
