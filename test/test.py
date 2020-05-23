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
        print("\nTesting that web pages are accessible...")
        routes = ("/", "/scheduler", "/times")
        # Use Flask test client
        with app.test_client() as client:
            for route in routes:
                print(f"\tChecking route {route}")
                response = client.get(route)
                self.assertEqual(response.status_code, 200)

class BusyTimesReporterTests(unittest.TestCase):
    pass

class SimulationManagerTests(unittest.TestCase):

    def test_simulated_data(self):
        """
        Tests proper reading of simulated data.
        """
        print("\nTesting proper reading of simulated data...")
        cases = ("park", "store") # TODO: , "supermarket", "restaurant")
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
             }]
        for case in cases:
            print(f"\tChecking type {case}")
            observed = SimulationManager.get_busy_times(case)
            expected = expected_results[cases.index(case)]
            self.assertEqual(observed, expected)
if __name__ == '__main__':
    unittest.main()
