import requests
import json
import multiprocessing
import calendar
import datetime
from data.apiHandler import apiKeyLoader
from flask_restful import Resource, reqparse, request
import data.bestTime as bestTime
from data.bestTime import bestTime


class bestPlace(Resource):
    def post(self):
        # Take the JSON from the request
        json_dump = request.get_json()
        print(json.dumps(json_dump, indent=4))

        # Setup Place_ID
        places = json_dump['place'][0]

        # Setup the day of the week
        today = datetime.datetime.today()
        day = calendar.day_name[today.weekday()]

        # Retrieve the best times and return it
        ret = self.get_best_place(places, day)
        return '', 200

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
        # setup multiprocessing
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

