import requests
import json
from data.apiHandler import apiKeyLoader
from flask_restful import Resource, reqparse, request
import multiprocessing
import data.bestTime as bestTime
from data.bestTime import bestTime


class bestPlace(Resource):
    def __init__(self):
        self.apiHandler = apiKeyLoader()
        self.req_parser = reqparse.RequestParser()
        self.req_parser.add_argument('latitude', type=float)
        self.req_parser.add_argument('longitude', type=float)
        self.req_parser.add_argument('text', type=str)

    def get(self, request):
        r = reqparse.RequestParser(request)
        return r, 200

    def add_api_arg(self):
        return "&key=" + self.apiHandler.get_api_key()

    def make_request(self, **kwargs):
        # load up our parameters
        package = "location=44.0448,-123.0726&radius=500&type=restaurant"+self.add_api_arg()

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

    @staticmethod
    def place_helper(d, location, day, test_list):
        '''
        wrapper for bestPlace call, assigns return to the proxydict.
        '''
        d[location] = bestTime.get_best_time(location, day, test_list)


    @staticmethod
    def get_best_place(locations, day, test_dict = None):
        '''
        list, string, dict(location: popularity) -> dict(location: (hour, popularity))
        Given a list of google maps placeid's and the day of the week, returns a dictionary of best times.
        '''
        #setup multiprocessing
        manager = multiprocessing.Manager()
        proxdict = manager.dict( { i : None for i in locations } )
        
        arglist = None
        if(test_dict is not None):
            try:
                arglist = [ (proxdict, x, day, test_dict[x]) for x in locations ]
            except KeyError as e:
                raise KeyError("locationid is not a key in test_dict")
        else:
            arglist = [ (proxdict, x, day, None) for x in locations ]

        with multiprocessing.Pool() as p:
            p.starmap(bestPlace.place_helper, arglist)

        result = proxdict.copy() #managers aren't cleaned up at scope exit, so we have to copy this here.
        manager.shutdown()

        return result

