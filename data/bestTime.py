"""
bestTime.py
===============================================================================
Last Modified: 22 May 2020
Modification By: Morgan Edlund
Creation Date: 22 May 2020
Initial Author: Bryan Carl
===============================================================================


"""
import requests
import json
from flask_restful import Resource, reqparse
import data.busy_times.reporter as time_reporter

class bestTime(Resource):
    def __init__(self):
        #self.apiHandler = api_handler #TODO Readd this to init
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

    def get_best_time(self, location, day, test_list = None):
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
        if(test_list is not None):
            if (len(test_list) is not 24):
                raise TypeError("Malformed list passed; needs 24 ints")
            times = test_list #Single list, so you don't have to type a full week's worth of info.
        else:
            reporter = time_reporter.BusyTimesReporter()
            result = reporter.get_busy_times(location, 1) #TODO: some sort of global or local var for busytimes mode selection
            times = result[day] #get the info, and then strip out what we need
        
        outlist = sorted(zip(hours, times), key=lambda pair: pair[1])
        return outlist



