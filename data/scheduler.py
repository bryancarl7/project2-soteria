import requests
from data.apiHandler import apiHandler
from flask_restful import Resource


class scheduler(Resource):
    def __init__(self, api_handler):
        self.apiHandler = api_handler
        self.id = ""
        self.table = []

    def get(self):
        return '', 200

    def post(self):
        return '', 200

    def delete(self):
        return '', 200

    def create(self):
        return '', 200