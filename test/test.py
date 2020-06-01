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

class ServerTests(unittest.TestCase):
    def test_server_pages(self):
        """
        Tests that all the web pages are accessible.
        """
        print()
        print("=" * 80)
        print("Testing that all web pages are accessible...")
        routes = ("/")
        # Use Flask test client
        with app.test_client() as client:
            for route in routes:
                print(f"\tChecking route {route}")
                response = client.get(route)
                self.assertEqual(response.status_code, 200)


    def test_server_resources(self):
        """
        Test server resources.
        """
        print()
        print("=" * 80)
        print("Testing that all web resources are accessible...")
        routes = ("/times/bestTime", "/times/bestPlace", "/scheduler/update")
        methods = ("POST", "POST", "POST")
        with app.test_client() as client:
            for route in routes:
                print(f"\tChecking resource {route}")
                response = None
                if route == "/scheduler/update":
                    response = client.post(route, json= {

                                "0": {
                                    "placeId": "ChIJy1J05GSHj4ARTvUR7hHkajg",
                                    "time": 120,
                                    "priority": "1",
                                    "type": [
                                        "park",
                                        "tourist_attraction",
                                        "point_of_interest",
                                        "establishment"
                                    ]
                                },
                                "1": {
                                    "placeId": "ChIJLx5Zf0N-hYARgSyH_pVY7rQ",
                                    "time": 129,
                                    "priority": "5",
                                    "type": [
                                        "restaurant",
                                        "food",
                                        "point_of_interest",
                                        "establishment"
                                    ]
                                }
                            }
                            )
                elif route == "/times/bestPlace":
                    response = client.post(route, json={
                                "placeId": [
                                    "ChIJycspTWsewVQR-6AWLn5b0SI",
                                    "ChIJo-lWcS8ewVQRBfpW0CZB-7I",
                                    "ChIJmWVWnREewVQRRS5lF9yW8FU",
                                    "ChIJO4Qk6X4dwVQRtWY2W1l3bZc",
                                    "ChIJM0hybxEewVQRujac4KF-fLo",
                                    "ChIJpVju6eQdwVQRsrGHuLxesxY",
                                    "ChIJB0XOu-wdwVQR3gEsw-n_aDw",
                                    "ChIJswlLbW0ewVQRqEcNPylhV3g",
                                    "ChIJ1UgjVwsewVQRFeYaTzCEgvA",
                                    "ChIJT3INGkMewVQRc4CGF9O2M4Q"
                                ],
                                "type": {
                                    "ChIJycspTWsewVQR-6AWLn5b0SI": [
                                        "bar",
                                        "restaurant",
                                        "food",
                                        "point_of_interest",
                                        "establishment"
                                    ],
                                    "ChIJo-lWcS8ewVQRBfpW0CZB-7I": [
                                        "restaurant",
                                        "food",
                                        "point_of_interest",
                                        "establishment"
                                    ],
                                    "ChIJmWVWnREewVQRRS5lF9yW8FU": [
                                        "bar",
                                        "restaurant",
                                        "food",
                                        "point_of_interest",
                                        "establishment"
                                    ],
                                    "ChIJO4Qk6X4dwVQRtWY2W1l3bZc": [
                                        "restaurant",
                                        "food",
                                        "point_of_interest",
                                        "establishment"
                                    ],
                                    "ChIJM0hybxEewVQRujac4KF-fLo": [
                                        "restaurant",
                                        "food",
                                        "point_of_interest",
                                        "establishment"
                                    ],
                                    "ChIJpVju6eQdwVQRsrGHuLxesxY": [
                                        "restaurant",
                                        "food",
                                        "point_of_interest",
                                        "establishment"
                                    ],
                                    "ChIJB0XOu-wdwVQR3gEsw-n_aDw": [
                                        "restaurant",
                                        "food",
                                        "point_of_interest",
                                        "establishment"
                                    ],
                                    "ChIJswlLbW0ewVQRqEcNPylhV3g": [
                                        "meal_takeaway",
                                        "restaurant",
                                        "food",
                                        "point_of_interest",
                                        "establishment"
                                    ],
                                    "ChIJ1UgjVwsewVQRFeYaTzCEgvA": [
                                        "restaurant",
                                        "food",
                                        "point_of_interest",
                                        "establishment"
                                    ],
                                    "ChIJT3INGkMewVQRc4CGF9O2M4Q": [
                                        "bar",
                                        "restaurant",
                                        "food",
                                        "point_of_interest",
                                        "establishment"
                                    ]
                                }

                            })
                else:
                    response = client.post(route, json={
                                "placeId": "ChIJxapf8PF_hYARPg1Ki7Ws9pE",
                                "location": {
                                    "lat": 37.8707458,
                                    "lng": -122.2731167
                                },
                                "type": [
                                    "cafe",
                                    "food",
                                    "point_of_interest",
                                    "establishment"
                                ]
                            }
                            )
                self.assertEqual(response.status_code, 200)

# Need to discuss:
# TODO: use unittest.mock when using requests OR Flask app.test_client()


class SimulationManagerTests(unittest.TestCase):

    def test_simulated_data(self):
        """
        Tests proper reading of simulated data.
        """
        print()
        print("=" * 80)
        print("Testing that simulated data sets are accessible...")
        cases = ("park", "store", "supermarket", "restaurant")
        expected_results = [
            {'Monday': [0, 0, 0, 0, 0, 0, 1, 4, 25, 31, 34, 42, 49, 50, 56, 61,
                     55, 37, 21, 11, 5, 2, 0, 0],
             'Tuesday': [0, 0, 0, 0, 0, 0, 1, 8, 24, 29, 36, 43, 44, 42, 44, 51,
                     48, 31, 16, 8, 1, 1, 0, 0],
             'Wednesday': [0, 0, 0, 0, 0, 0, 1, 3, 15, 23, 33, 36, 33, 29, 36, 40,
                     37, 29, 19, 11, 5, 4, 0, 0],
             'Thursday': [0, 0, 0, 0, 0, 0, 3, 5, 19, 29, 39, 43, 40, 35, 39, 52,
                     50, 30, 13, 5, 2, 0, 0, 0],
             'Friday': [0, 0, 0, 0, 0, 0, 1, 7, 22, 30, 35, 41, 44, 46, 50, 58,
                     53, 33, 19, 13, 10, 8, 0, 0],
             'Saturday': [0, 0, 0, 0, 0, 0, 1, 1, 14, 26, 39, 63, 63, 62, 83, 99,
                     83, 52, 29, 16, 6, 4, 0, 0],
             'Sunday': [0, 0, 0, 0, 0, 0, 1, 1, 6, 18, 36, 53, 61, 64, 68, 70, 61,
                     42, 23, 11, 4, 2, 0, 0]
             },
            {'Monday': [0, 0, 0, 0, 0, 0, 5, 16, 26, 36, 43, 47, 49, 52, 53, 52,
                     50, 49, 49, 45, 28, 0, 0, 0],
             'Tuesday': [0, 0, 0, 0, 0, 0, 8, 21, 32, 40, 53, 60, 62, 60, 57, 55,
                     53, 53, 53, 38, 22, 0, 0, 0],
             'Wednesday': [0, 0, 0, 0, 0, 0, 7, 22, 35, 43, 55, 60, 60, 57, 52, 47,
                     44, 45, 46, 32, 19, 0, 0, 0],
             'Thursday': [0, 0, 0, 0, 0, 0, 5, 17, 27, 35, 49, 57, 60, 57, 53, 50,
                     49, 50, 51, 36, 21, 0, 0, 0],
             'Friday': [0, 0, 0, 0, 0, 0, 7, 21, 31, 38, 53, 57, 58, 59, 59, 56,
                     53, 53, 53, 33, 18, 0, 0, 0],
             'Saturday': [0, 0, 0, 0, 0, 0, 4, 15, 26, 38, 71, 85, 91, 92, 92, 89,
                     80, 72, 63, 34, 19, 0, 0, 0],
             'Sunday': [0, 0, 0, 0, 0, 0, 0, 9, 17, 27, 53, 72, 85, 89, 88, 87,
                     82, 71, 56, 32, 20, 0, 0, 0]
             },
            {'Monday': [0, 0, 0, 0, 0, 0, 4, 9, 16, 24, 48, 57, 61, 60, 59, 65,
                     75, 78, 67, 46, 26, 17, 0, 0],
             'Tuesday': [0, 0, 0, 0, 0, 0, 7, 14, 21, 38, 48, 59, 67, 70, 67, 65,
                     69, 72, 67, 52, 29, 16, 0, 0],
             'Wednesday': [0, 0, 0, 0, 0, 0, 4, 8, 14, 21, 39, 47, 52, 53, 52, 52,
                     56, 57, 51, 40, 26, 19, 0, 0],
             'Thursday': [0, 0, 0, 0, 0, 0, 6, 14, 19, 30, 41, 51, 58, 58, 56, 56,
                     59, 60, 55, 44, 27, 17, 0, 0],
             'Friday': [0, 0, 0, 0, 0, 0, 9, 16, 23, 29, 52, 61, 67, 69, 66, 65,
                     66, 68, 62, 48, 28, 19, 0, 0],
             'Saturday': [0, 0, 0, 0, 0, 0, 4, 9, 17, 40, 58, 72, 80, 83, 83, 84,
                     88, 84, 67, 45, 26, 21, 0, 0],
             'Sunday': [0, 0, 0, 0, 0, 0, 5, 12, 21, 31, 55, 70, 82, 91, 95, 98,
                     97, 83, 60, 32, 21, 12, 0, 0]
             },
            {'Monday': [12, 0, 0, 0, 0, 0, 0, 0, 4, 8, 16, 31, 40, 44, 28, 26, 27,
                     33, 41, 43, 36, 19, 17, 13],
             'Tuesday': [7, 0, 0, 0, 0, 0, 0, 0, 5, 9, 16, 32, 41, 42, 25, 20, 21,
                     30, 39, 41, 34, 17, 16, 14],
             'Wednesday': [9, 0, 0, 0, 0, 0, 0, 0, 5, 8, 18, 33, 40, 36, 17, 15, 19,
                     28, 36, 39, 35, 18, 13, 8],
             'Thursday': [4, 0, 0, 0, 0, 0, 0, 0, 3, 7, 13, 27, 37, 38, 25, 20, 21,
                     30, 42, 45, 37, 17, 18, 16],
             'Friday': [10, 0, 0, 0, 0, 0, 0, 0, 6, 10, 16, 32, 43, 46, 31, 29,
                     32, 42, 52, 55, 52, 23, 21, 20],
             'Saturday': [14, 6, 0, 0, 0, 0, 0, 0, 8, 16, 34, 56, 69, 71, 48, 44,
                     44, 52, 62, 62, 49, 20, 21, 21],
             'Sunday': [15, 7, 0, 0, 0, 0, 0, 0, 0, 0, 9, 27, 43, 52, 50, 43, 42,
                     51, 61, 56, 40, 16, 15, 16]
             }
            ]
        for case in cases:
            print(f"\tChecking type {case}")
            observed, flag = SimulationManager.get_busy_times(case)
            expected = expected_results[cases.index(case)]
            self.assertEqual(observed, expected)

class BusyTimesReporterTests(unittest.TestCase):

    def test_get_api_key(self):
        print()
        print("=" * 80)
        print("Testing the functionality of reporter API")
        result = BusyTimesReporter.get_api_key()
        self.assertIsNotNone(result)

    def test_get_busy_times(self):
        modeType = [BusyTimesReporter.Mode.SIMULATED,
                    BusyTimesReporter.Mode.ACCURATE] # simulated, accurate
        locations = ["ChIJSYuuSx9awokRyrrOFTGg0GY"]
        for location in locations:
            for mode in modeType:
                print("Checking for location:", location, ", mode type:", mode)
                result, flag = BusyTimesReporter.get_busy_times(location, mode, ["restauran"])
                print(f"Flag {flag}")
                if mode == BusyTimesReporter.Mode.SIMULATED: # Change when simulated working
                    result = True
                self.assertIsNotNone(result)

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
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        print("For bestPlace, \n")
        print("Checking for the result of today for all locations")
        print("Checking for location:", locations)
        for location in locations:
            real_result = bp.get_best_place(locations, days[date_index])[0]
            #print("real result:", real_result)
            self.assertEqual(len(locations), len(real_result))

if __name__ == '__main__':
    print("It will take a couple of minutes for testing")
    unittest.main()
