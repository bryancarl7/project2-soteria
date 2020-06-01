"""
test.py

===============================================================================

Last Modified: 31 May 2020
Modification By: Jinhu Qi

Creation Date: 15 May 2020
Initial Author: Bryan Carl

===============================================================================

This module contains all the unit and integration tests for the system. Because
of this, it interfaces with every single module.
"""

# Standard Imports
import time
import unittest
from unittest import mock

# Third Party Packages
import requests

# Local Modules

from data.busy_times.reporter import BusyTimesReporter
from data.busy_times.manager import SimulationManager
from server.api import app, PORT, ENV, HOST
from data.bestTime import bestTime
from data.bestPlace import bestPlace
from flask_restful import request
from datetime import date


class BestTimeTests(unittest.TestCase):

    # test a place types department store, grocery or supermarket, electronics_store, furniture_store
    def test_get_best_time_1(self):
        print()
        print("=" * 80)
        print("Testing the functionality of BestTime API")
        print("Testing  get best time function")
        bt = bestTime()
        locations = ["ChIJcWPM1VYRkFQRpjilF_m5vew"]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        print("For bestTime, \n")
        expected_result = 24
        for location in locations:
            for day in days:
                print("Checking for location:", location, ", days:", day)
                result = bt.get_best_time(location, day, ["department_store", "grocery_or_supermarket", "electronics_store", "furniture_store"])[0]
                self.assertEqual(len(result), expected_result)

    # test a place type locality, political
    def test_get_best_time_2(self):
        print()
        print("=" * 80)
        print("Testing the functionality of BestTime API")
        print("Testing  get best time function")
        bt = bestTime()
        locations = ["ChIJMz0NgmbBxokREdZcZuO-TWE"]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        print("For bestTime, \n")
        expected_result = 24
        for location in locations:
            for day in days:
                print("Checking for location:", location, ", days:", day)
                result = bt.get_best_time(location, day, ["locality", "political"])[0]
                self.assertEqual(len(result), expected_result)

    # test a place type point of interest, establishment
    def test_get_best_time_3(self):
        print()
        print("=" * 80)
        print("Testing the functionality of BestTime API")
        print("Testing  get best time function")
        bt = bestTime()
        locations = ["ChIJsQLp1UUVkFQRDtojPV9uMSY"]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        print("For bestTime, \n")
        expected_result = 24
        for location in locations:
            for day in days:
                print("Checking for location:", location, ", days:", day)
                result = bt.get_best_time(location, day, ["point_of_interest", "establishment"])[0]
                self.assertEqual(len(result), expected_result)

class BestPlaceTests(unittest.TestCase):

    def test_get_best_place_1(self):
        print()
        print("=" * 80)
        print("Testing the functionality of BestPlace API")
        print("Testing  get best place function")
        bp = bestPlace()
        locations = ["ChIJNVdWgfiglVQRSuD8w0aQGrk",
                     "ChIJLbTuxOqglVQRXgWNWDb3baI",
                     "ChIJVxwSAjUKlVQRO7flVL8N8m4",
                     "ChIJBa0HbWinlVQRpstaBx75aMs",
                     "ChIJGfTXCycKlVQRe9loilMSQG4",
                     "ChIJE-AuCv4JlVQR5ZQW0fPD244",
                     "ChIJr6EmzR6olVQRReWCk4FdUvc",
                     "ChIJ5aJvEA8KlVQRf_H2D-kqjIc",
                     "ChIJG3ungAinlVQRY4qQAC-c6SM",
                     "ChIJCZxxVjuhlVQRZmUU9vAIJg4"]

        date_index = date.today().weekday()
        days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

        print("For bestPlace, \n")
        print("Checking for the result of today for all locations")
        print("Checking for location:", locations)
        for location in locations:
            real_result = bp.get_best_place(locations, days[date_index])[0]
            #print("real result:", real_result)
            self.assertEqual(len(locations), len(real_result))

if __name__ == '__main__':
    unittest.main()
