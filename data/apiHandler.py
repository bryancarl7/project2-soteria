import json
from flask_restful import Resource


class apiHandler(Resource):
    def __init__(self, port, host, env, file):
        self.port = port
        self.host = host
        self.env = env
        self.config_file = file
        self.api_key = ""
        self.setup_credentials()

    def setup_credentials(self):
        with open(self.config_file) as json_cred:
            credentials = json.load(json_cred)
        self.api_key = credentials["API_Key"]