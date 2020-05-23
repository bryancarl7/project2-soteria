"""
reporter.py
===============================================================================
Last Modified: 22 May 2020
Modification By: Carter Perkins
Creation Date: 21 May 2020
Initial Author: Carter Perkins
===============================================================================
This module returns the relative "business" of a location, defined in the SDS
Section 4.1 - Busy Times Reporter, for scheduling and optimal time algorithms
utilized in the Flask API (aforementioned module is defined in the SDS Section
4.2 - Flask API). Due to this design, the Busy Times Reporter is completely
independent of all other modules.
In short, this reporting module utilizes two modes, accurate and simulated, to
determine how congested a particular location is. It utilizes the Google Maps
Place API for location data, and the 'Popular times' package to scrape the
Google Maps "Busy Times" information. Also, the simulated dataset is built
referencing the "Busy Times" data.
"""
import requests
import json
from flask_restful import Resource, reqparse
import data.busy_times.reporter as time_reporter

class bestTime(Resource):
    def __init__(self):
        #self.apiHandler = api_handler #TODO Read this to init
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




