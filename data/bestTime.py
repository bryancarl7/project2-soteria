import requests
import json
from flask_restful import Resource, reqparse


class bestTime(Resource):
    def __init__(self, api_handler):
        self.apiHandler = api_handler
        self.id = ""

    def get(self, request):
        r = reqparse.RequestParser(request)
        return r, 200

    def make_request(self, **kwargs):
        # load up our parameters
        package = "location=44.0448,-123.0726&radius=500&type=restaurant" + \
                  "&key=" + self.api

        # map out our url to be loaded
        new_request_url = ("https://maps.googleapis.com/maps/api/" +
                           "place/nearbysearch/json?{}".format(package))
        print(new_request_url)

        # open the url as a response to be read from
        with requests.get(new_request_url) as response:
            # Print the json nicely
            html = response.json()
            parsed = json.loads(html)
            print(json.dumps(parsed, indent=4))
            print(response)
            print(len(parsed["results"]))
            return parsed