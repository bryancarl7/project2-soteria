"""
bestPlace.py
===============================================================================
Last Modified: 1 June 2020
Modification By: Morgan Edlund
Creation Date: 22 May 2020
Initial Author: Bryan Carl
===============================================================================
"""
import json
import multiprocessing
import calendar
import datetime
from flask_restful import Resource, reqparse, request
import data.bestTime as bestTime
from data.bestTime import bestTime


class bestPlace(Resource):
    def post(self):
        # Take the JSON from the request
        json_dump = request.get_json()
        print(json.dumps(json_dump, indent=4))

        # Setup Place_ID
        places = json_dump['placeId']
        types = json_dump['type']

        # Setup the day of the week
        today = datetime.datetime.today()
        day = calendar.day_name[today.weekday()]

        # Retrieve the best times and return it
        ret = self.get_best_place(places, day, types)
        return ret, 200

    @staticmethod
    def place_helper(d, location, day, types_dict, test_list):
        '''
        wrapper for bestPlace call, assigns return to the proxydict.
        '''
        ret, flag = bestTime.get_best_time(location, day, types_dict, test_list)
        #print(flag)
        d[location] = ret
        d[(location + "flag")] = flag

    @staticmethod
    def get_best_place(locations, day, types_dict = None, test_dict = None):
        '''
        list, string, dict(location: popularity) -> dict(location: (hour, popularity))
        Given a list of google maps placeid's and the day of the week, returns a dictionary of best times.
        '''
        # setup multiprocessing
        manager = multiprocessing.Manager()
        proxdict = manager.dict( { i : None for i in locations } )
        simkeys = {}
        arglist = None
        if types_dict is None:
            types_dict = {x:[] for x in locations}
        if(test_dict is not None):
            try:
                arglist = [ (proxdict, x, day, types_dict[x], test_dict[x]) for x in locations ]
            except KeyError as e:
                raise KeyError("locationid is not a key in test_dict")
        else:
            arglist = [ (proxdict, x, day, types_dict[x], None) for x in locations ]

        with multiprocessing.Pool() as p:
            p.starmap(bestPlace.place_helper, arglist)

        result = proxdict.copy() #managers aren't cleaned up at scope exit, so we have to copy this here.
        manager.shutdown()
        for loc in locations:
            simkeys[loc] = result.pop( (loc+"flag") )

        return result, simkeys

