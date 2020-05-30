"""

===============================================================================

Last Modified: 26 May 2020
Modification By: Jinhu Qi

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

# class BestTimeTests(unittest.TestCase):
#
#     def test_get_best_time_1(self):
#         print()
#         print("=" * 80)
#         print("Testing the functionality of BestTime API")
#         print("Testing  get best time function")
#         bt = bestTime()
#         locations = ["ChIJa147K9HX3IAR-lwiGIQv9i4"]
#         days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
#         print("For bestTime, \n")
#         #expected_result = {'Monday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 39, 53, 46, 31, 27, 38, 55, 61, 50, 29, 12, 0, 0],
#         #                   'Tuesday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 28, 43, 40, 29, 31, 48, 68, 70, 55, 33, 17, 0, 0],
#         #                   'Wednesday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 18, 32, 35, 27, 21, 31, 51, 57, 40, 18, 5, 0, 0],
#         #                  'Thursday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 28, 50, 44, 30, 33, 50, 64, 65, 52, 32, 16, 0, 0],
#         #                   'Friday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 21, 28, 29, 25, 32, 67, 100, 83, 48, 35, 24, 10, 0],
#         #                   'Saturday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 16, 42, 57, 40, 27, 33, 48, 59, 57, 44, 28, 14, 0],
#         #                   'Sunday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 23, 31, 37, 42, 52, 66, 78, 73, 57, 50, 46, 31, 0, 0]}
#
#         expected_result = [(6, 4), (7, 15), (20, 19), (8, 26), (19, 34), (9, 38), (18, 63), (10, 71), (17, 72), (16, 80), (11, 85), (15, 89), (12, 91), (13, 92), (14, 92), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (21, 0), (22, 0), (23, 0)]
#         for location in locations:
#             for day in days:
#                 print("Checking for location:", location, ", days:", day)
#                 result = bt.get_best_time(location, day)
#                 print("expected result: ", expected_result)
#                 print("real result: ", result)
#                 self.assertEqual(result, expected_result)

class BestPlaceTests(unittest.TestCase):

    def test_get_best_place_1(self):
        print()
        print("=" * 80)
        print("Testing the functionality of BestPlace API")
        print("Testing  get best place function")
        bp = bestPlace()
        locations = ["ChIJs2Lkp0Xc3IARt2AnTeAM9Jk",
                     "ChIJHZ2y2vfn3IARApEK9qYdNGQ",
                     "ChIJIUcczmDe3IARzC_90ctUBW8",
                     "ChIJHRL3_Zze3IAR0KMmrDzh2tM",
                     "ChIJRQHY3Bzd3IARkZI4FfXygg0"]

        days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

        print("For bestPlace, \n")
        #expected_result = {'Monday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 39, 53, 46, 31, 27, 38, 55, 61, 50, 29, 12, 0, 0],
        #                   'Tuesday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 28, 43, 40, 29, 31, 48, 68, 70, 55, 33, 17, 0, 0],
        #                   'Wednesday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 18, 32, 35, 27, 21, 31, 51, 57, 40, 18, 5, 0, 0],
        #                  'Thursday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 28, 50, 44, 30, 33, 50, 64, 65, 52, 32, 16, 0, 0],
        #                   'Friday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 21, 28, 29, 25, 32, 67, 100, 83, 48, 35, 24, 10, 0],
        #                   'Saturday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 16, 42, 57, 40, 27, 33, 48, 59, 57, 44, 28, 14, 0],
        #                   'Sunday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 23, 31, 37, 42, 52, 66, 78, 73, 57, 50, 46, 31, 0, 0]}

        expected_results = [{'Monday': [0, 0, 0, 0, 0, 0, 7, 21, 50, 78, 100, 92, 85, 71, 50, 28, 0, 0, 0, 0, 0, 0, 0, 0], 'Tuesday': [0, 0, 0, 0, 0, 0, 14, 21, 28, 35, 42, 50, 42, 42, 28, 21, 0, 0, 0, 0, 0, 0, 0, 0], 'Wednesday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Thursday': [0, 0, 0, 0, 0, 0, 7, 28, 71, 85, 42, 21, 57, 64, 14, 7, 0, 0, 0, 0, 0, 0, 0, 0], 'Friday': [0, 0, 0, 0, 0, 0, 7, 28, 78, 100, 57, 42, 71, 92, 78, 50, 0, 0, 0, 0, 0, 0, 0, 0], 'Saturday': [0, 0, 0, 0, 0, 0, 0, 14, 28, 42, 64, 78, 85, 71, 57, 42, 0, 0, 0, 0, 0, 0, 0, 0], 'Sunday': [0, 0, 0, 0, 0, 0, 0, 0, 50, 71, 64, 42, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
                            {'Monday': [0, 0, 0, 0, 0, 0, 0, 14, 28, 36, 38, 36, 34, 28, 16, 6, 0, 0, 0, 0, 0, 0, 0, 0], 'Tuesday': [0, 0, 0, 0, 0, 0, 0, 20, 40, 46, 44, 48, 40, 22, 10, 6, 0, 0, 0, 0, 0, 0, 0, 0], 'Wednesday': [0, 0, 0, 0, 0, 0, 0, 10, 18, 26, 32, 34, 30, 24, 16, 10, 0, 0, 0, 0, 0, 0, 0, 0], 'Thursday': [0, 0, 0, 0, 0, 0, 0, 24, 36, 44, 58, 54, 36, 22, 16, 10, 0, 0, 0, 0, 0, 0, 0, 0], 'Friday': [0, 0, 0, 0, 0, 0, 0, 32, 64, 70, 52, 40, 36, 32, 24, 16, 0, 0, 0, 0, 0, 0, 0, 0], 'Saturday': [0, 0, 0, 0, 0, 0, 0, 0, 38, 64, 76, 68, 52, 40, 32, 26, 0, 0, 0, 0, 0, 0, 0, 0], 'Sunday': [0, 0, 0, 0, 0, 0, 0, 0, 58, 100, 78, 54, 54, 52, 42, 26, 0, 0, 0, 0, 0, 0, 0, 0]},
                            {'Monday': [0, 0, 0, 0, 0, 0, 7, 22, 34, 34, 30, 37, 47, 51, 46, 35, 24, 23, 34, 50, 50, 0, 0, 0], 'Tuesday': [0, 0, 0, 0, 0, 0, 6, 15, 25, 27, 28, 38, 50, 47, 34, 26, 30, 38, 43, 40, 30, 0, 0, 0], 'Wednesday': [0, 0, 0, 0, 0, 0, 2, 16, 34, 26, 27, 41, 52, 53, 46, 34, 26, 28, 34, 38, 36, 0, 0, 0], 'Thursday': [0, 0, 0, 0, 0, 0, 6, 30, 49, 36, 35, 57, 75, 73, 54, 33, 22, 23, 31, 37, 37, 0, 0, 0], 'Friday': [0, 0, 0, 0, 0, 0, 27, 53, 52, 33, 38, 73, 100, 90, 56, 34, 35, 50, 66, 71, 63, 0, 0, 0], 'Saturday': [0, 0, 0, 0, 0, 0, 9, 39, 74, 71, 52, 55, 69, 79, 77, 66, 53, 46, 47, 52, 53, 0, 0, 0], 'Sunday': [0, 0, 0, 0, 0, 0, 0, 7, 22, 46, 75, 96, 97, 84, 71, 62, 58, 60, 66, 69, 58, 0, 0, 0]},
                            {'Monday': [0, 0, 0, 0, 0, 0, 0, 0, 21, 36, 52, 52, 47, 31, 21, 15, 26, 31, 36, 31, 21, 0, 0, 0], 'Tuesday': [0, 0, 0, 0, 0, 0, 0, 15, 26, 42, 47, 42, 26, 21, 21, 26, 36, 36, 31, 21, 10, 0, 0, 0], 'Wednesday': [0, 0, 0, 0, 0, 0, 0, 0, 15, 36, 36, 31, 36, 36, 26, 21, 21, 26, 26, 21, 10, 0, 0, 0], 'Thursday': [0, 0, 0, 0, 0, 0, 0, 10, 15, 21, 26, 31, 36, 36, 36, 36, 31, 26, 21, 15, 10, 0, 0, 0], 'Friday': [0, 0, 0, 0, 0, 0, 0, 15, 21, 31, 36, 42, 42, 36, 31, 31, 31, 36, 42, 47, 36, 26, 15, 0], 'Saturday': [0, 0, 0, 0, 0, 0, 0, 0, 26, 57, 84, 100, 100, 89, 84, 78, 63, 47, 31, 21, 26, 42, 36, 0], 'Sunday': [0, 0, 0, 0, 0, 0, 0, 0, 31, 47, 57, 63, 57, 57, 52, 42, 42, 47, 42, 31, 15, 0, 0, 0]},
                            {'Monday': [0, 0, 0, 0, 0, 0, 0, 38, 65, 73, 65, 57, 61, 69, 65, 57, 53, 53, 46, 26, 11, 0, 0, 0], 'Tuesday': [0, 0, 0, 0, 0, 0, 0, 19, 34, 34, 30, 46, 65, 61, 38, 26, 46, 80, 80, 46, 11, 0, 0, 0], 'Wednesday': [0, 0, 0, 0, 0, 0, 0, 38, 50, 42, 38, 50, 57, 57, 46, 42, 46, 57, 65, 57, 38, 0, 0, 0], 'Thursday': [0, 0, 0, 0, 0, 0, 0, 50, 80, 84, 88, 100, 96, 76, 73, 80, 88, 84, 76, 61, 42, 0, 0, 0], 'Friday': [0, 0, 0, 0, 0, 0, 0, 11, 26, 50, 69, 73, 65, 50, 46, 57, 76, 88, 80, 61, 38, 0, 0, 0], 'Saturday': [0, 0, 0, 0, 0, 0, 0, 11, 46, 88, 88, 76, 88, 100, 92, 76, 61, 53, 42, 34, 23, 0, 0, 0], 'Sunday': [0, 0, 0, 0, 0, 0, 0, 0, 26, 46, 69, 80, 80, 69, 46, 26, 23, 57, 30, 42, 57, 0, 0, 0]}
                            ]
        result = []
        for day in days:
            #print("Checking for location:", locations, ", days:", day)
            result.append(bp.get_best_place(locations, day))

        print("expected result: ", expected_results)
        print("real result: ", result)

        self.assertEqual(result, expected_results)

if __name__ == '__main__':
    unittest.main()

