"""
bestTime.py
===============================================================================
Last Modified: 25 May 2020
Modification By: Bryan Carl
Creation Date: 22 May 2020
Initial Author: Bryan Carl
===============================================================================
"""
import json
from flask_restful import Resource, reqparse, request
import data.busy_times.reporter as time_reporter
from data.apiHandler import apiKeyLoader
import datetime
import calendar


class bestTime(Resource):
    def post(self):
        # Take the JSON from the request
        json_dump = request.get_json()
        print(json.dumps(json_dump, indent=4))

        # Setup Place_ID
        places = json_dump['placeId']
        location = json_dump['location']

        # Setup the day of the week
        today = datetime.datetime.today()
        day = calendar.day_name[today.weekday()]

        # Retrieve the best times and return it
        ret = self.get_best_time(places, day)
        return ret, 200

    @staticmethod
    def get_best_time(location, day, test_list=None):
        '''
        string(google places API placeid), string(name of day), (optional) 0-100 ratio int list -> (hour, ratio) list
        Returns a sorted list of times to visit a given location, with times of lowest relative population sorted first.
        if test_list is specified, it will validate and use that data for the returned list (allows for testing of logic).
        
        Each pair in the returned list is in the format of (hour in military time, 0-100 ratio rating of relative business). 

        Raises:
            TypeError when test_list specified and doesn't have 24 ints

        '''
        times = None
        hours = [i for i in range(24)]
        if test_list:
            if len(test_list) != 24:
                raise TypeError("Malformed list passed; needs 24 ints")
            times = test_list #Single list, so you don't have to type a full week's worth of info.
        else:
            reporter = time_reporter.BusyTimesReporter()
            result = reporter.get_busy_times(location, 1) #TODO: some sort of global or local var for busytimes mode selection
            times = result[day] #get the info, and then strip out what we need
        
        outlist = sorted(zip(hours, times), key=lambda pair: 1000 if pair[1] == 0 else pair[1] )
        return outlist




