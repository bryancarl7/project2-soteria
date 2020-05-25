"""
test.py

===============================================================================

Last Modified: 23 May 2020
Modification By: Carter Perkins

Creation Date: 15 May 2020
Initial Author: Bryan Carl

===============================================================================

This module contains all the unit and integration tests for the system. Because
of this, it interfaces with every single module.
"""

# Standard Imports
import time
import unittest

# Third Party Packages
import requests

# Local Modules
from data.busy_times.reporter import BusyTimesReporter
from data.busy_times.manager import SimulationManager
from server.api import app, PORT, ENV, HOST, apiHandler

class ServerTests(unittest.TestCase):

    def test_server_pages(self):
        """
        Tests that all the web pages are accessible.
        """
        print()
        print("=" * 80)
        print("Testing that all web pages are accessible...")
        routes = ("/", "/scheduler", "/times")
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
        with app.test_client() as client:
            for route in routes:
                print(f"\tChecking resource {route} via HTTP Get")
                response = client.get(route)
                self.assertEqual(response.status_code, 200)

# Need to discuss:
# TODO: use unittest.mock when using requests OR Flask app.test_client()

class BusyTimesReporterTests(unittest.TestCase):
    pass

class SimulationManagerTests(unittest.TestCase):
    """
    def test_bestTime(self):
        bT = bestTime(apiHandler)
        parsed = bT.make_request()
        self.assertIsNotNone(parsed)

    def test_bestPlace(self):
        bP = bestPlace(apiHandler)
        parsed = bP.make_request()
        self.assertIsNotNone(parsed)
    @classmethod
    def test_apiBestPlace(cls):
        response_place = requests.get("http://0.0.0.0:3000/times/bestPlace")
        assert(response_place.status_code, 200)
        print("best place page successfully created")


    @classmethod
    def test_apiBestTime(cls):
        response_time = requests.get("http://0.0.0.0:3000/times/bestTime")
        assert(response_time.status_code, 200)
        print("best time page successfully created")


    @classmethod
    def test_apiBestScheduler(cls):
        response_scheduler = requests.get("http://0.0.0.0:3000/scheduler/update")
        assert(response_scheduler.status_code, 200)
        print("scheduler page successfully created")
    """

    def test_simulated_data(self):
        """
        Tests proper reading of simulated data.
        """
        print()
        print("=" * 80)
        print("Testing that simulated data sets are accessible...")
        cases = ("park", "store", "supermarket", "restaurant")
        expected_results = [
            {'Mon': [0, 0, 0, 0, 0, 0, 1, 4, 25, 31, 34, 42, 49, 50, 56, 61,
                     55, 37, 21, 11, 5, 2, 0, 0],
             'Tue': [0, 0, 0, 0, 0, 0, 1, 8, 24, 29, 36, 43, 44, 42, 44, 51,
                     48, 31, 16, 8, 1, 1, 0, 0],
             'Wed': [0, 0, 0, 0, 0, 0, 1, 3, 15, 23, 33, 36, 33, 29, 36, 40,
                     37, 29, 19, 11, 5, 4, 0, 0],
             'Thu': [0, 0, 0, 0, 0, 0, 3, 5, 19, 29, 39, 43, 40, 35, 39, 52,
                     50, 30, 13, 5, 2, 0, 0, 0],
             'Fri': [0, 0, 0, 0, 0, 0, 1, 7, 22, 30, 35, 41, 44, 46, 50, 58,
                     53, 33, 19, 13, 10, 8, 0, 0],
             'Sat': [0, 0, 0, 0, 0, 0, 1, 1, 14, 26, 39, 63, 63, 62, 83, 99,
                     83, 52, 29, 16, 6, 4, 0, 0],
             'Sun': [0, 0, 0, 0, 0, 0, 1, 1, 6, 18, 36, 53, 61, 64, 68, 70, 61,
                     42, 23, 11, 4, 2, 0, 0]
             },
            {'Mon': [0, 0, 0, 0, 0, 0, 5, 16, 26, 36, 43, 47, 49, 52, 53, 52,
                     50, 49, 49, 45, 28, 0, 0, 0],
             'Tue': [0, 0, 0, 0, 0, 0, 8, 21, 32, 40, 53, 60, 62, 60, 57, 55,
                     53, 53, 53, 38, 22, 0, 0, 0],
             'Wed': [0, 0, 0, 0, 0, 0, 7, 22, 35, 43, 55, 60, 60, 57, 52, 47,
                     44, 45, 46, 32, 19, 0, 0, 0],
             'Thu': [0, 0, 0, 0, 0, 0, 5, 17, 27, 35, 49, 57, 60, 57, 53, 50,
                     49, 50, 51, 36, 21, 0, 0, 0],
             'Fri': [0, 0, 0, 0, 0, 0, 7, 21, 31, 38, 53, 57, 58, 59, 59, 56,
                     53, 53, 53, 33, 18, 0, 0, 0],
             'Sat': [0, 0, 0, 0, 0, 0, 4, 15, 26, 38, 71, 85, 91, 92, 92, 89,
                     80, 72, 63, 34, 19, 0, 0, 0],
             'Sun': [0, 0, 0, 0, 0, 0, 0, 9, 17, 27, 53, 72, 85, 89, 88, 87,
                     82, 71, 56, 32, 20, 0, 0, 0]
             },
            {'Mon': [0, 0, 0, 0, 0, 0, 4, 9, 16, 24, 48, 57, 61, 60, 59, 65,
                     75, 78, 67, 46, 26, 17, 0, 0],
             'Tue': [0, 0, 0, 0, 0, 0, 7, 14, 21, 38, 48, 59, 67, 70, 67, 65,
                     69, 72, 67, 52, 29, 16, 0, 0],
             'Wed': [0, 0, 0, 0, 0, 0, 4, 8, 14, 21, 39, 47, 52, 53, 52, 52,
                     56, 57, 51, 40, 26, 19, 0, 0],
             'Thu': [0, 0, 0, 0, 0, 0, 6, 14, 19, 30, 41, 51, 58, 58, 56, 56,
                     59, 60, 55, 44, 27, 17, 0, 0],
             'Fri': [0, 0, 0, 0, 0, 0, 9, 16, 23, 29, 52, 61, 67, 69, 66, 65,
                     66, 68, 62, 48, 28, 19, 0, 0],
             'Sat': [0, 0, 0, 0, 0, 0, 4, 9, 17, 40, 58, 72, 80, 83, 83, 84,
                     88, 84, 67, 45, 26, 21, 0, 0],
             'Sun': [0, 0, 0, 0, 0, 0, 5, 12, 21, 31, 55, 70, 82, 91, 95, 98,
                     97, 83, 60, 32, 21, 12, 0, 0]
             },
            {'Mon': [12, 0, 0, 0, 0, 0, 0, 0, 4, 8, 16, 31, 40, 44, 28, 26, 27,
                     33, 41, 43, 36, 19, 17, 13],
             'Tue': [7, 0, 0, 0, 0, 0, 0, 0, 5, 9, 16, 32, 41, 42, 25, 20, 21,
                     30, 39, 41, 34, 17, 16, 14],
             'Wed': [9, 0, 0, 0, 0, 0, 0, 0, 5, 8, 18, 33, 40, 36, 17, 15, 19,
                     28, 36, 39, 35, 18, 13, 8],
             'Thu': [4, 0, 0, 0, 0, 0, 0, 0, 3, 7, 13, 27, 37, 38, 25, 20, 21,
                     30, 42, 45, 37, 17, 18, 16],
             'Fri': [10, 0, 0, 0, 0, 0, 0, 0, 6, 10, 16, 32, 43, 46, 31, 29,
                     32, 42, 52, 55, 52, 23, 21, 20],
             'Sat': [14, 6, 0, 0, 0, 0, 0, 0, 8, 16, 34, 56, 69, 71, 48, 44,
                     44, 52, 62, 62, 49, 20, 21, 21],
             'Sun': [15, 7, 0, 0, 0, 0, 0, 0, 0, 0, 9, 27, 43, 52, 50, 43, 42,
                     51, 61, 56, 40, 16, 15, 16]
             }
            ]
        for case in cases:
            print(f"\tChecking type {case}")
            observed = SimulationManager.get_busy_times(case)
            expected = expected_results[cases.index(case)]
            self.assertEqual(observed, expected)

if __name__ == '__main__':
    unittest.main()
