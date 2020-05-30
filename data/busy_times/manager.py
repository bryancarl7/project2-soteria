"""
manager.py

===============================================================================

Last Modified: 29 May 2020
Modification By: Carter Perkins

Creation Date: 22 May 2020
Initial Author: Carter Perkins

===============================================================================

This is a submodule of the Busy Times Reporter that handles interactions with
the simulated data. Although independent, this component should only interface
with the driver of the larger module found in 'reporter.py'.
"""

# Standard Imports
import csv
import enum
import os

class SimulationManager():
    """
    The SimulationManager class is the interface for reading simulated data.
    """

    # Setup data file paths
    path = "/simulated_data/"
    files = (path + "food.csv", path + "grocery.csv", path + "parks.csv",
             path + "store.csv")

    @classmethod
    def get_busy_times(cls, location_types):
        """
        Returns the simulated busy time interval for a location type.

        Arguments:
            location_types  (List String)   - Location Type
        Returns:
            Dictionary                      - Busy Time Intervals
                Key         (String)        - Day of the Week
                Value       (Int List)      - Hour Occupancy Ratios
            Boolean                         - True if matching inaccurate
        Raises:
            ValueError                      - location_types invalid
            FileNotFoundError               - Missing simulated data file(s)
        """

        # https://developers.google.com/places/supported_types
        # TODO: Smart type to simulated filter
        valid_location_types = {"restaurant": cls.files[0],
                                "store": cls.files[3],
                                "supermarket": cls.files[1],
                                "park": cls.files[2]}

        # Validate data files
        BASE_DIR = os.path.dirname(os.path.realpath(__file__))
        for dataset in cls.files:
            if not os.path.isfile(f"{BASE_DIR}{dataset}"):
                raise FileNotFoundError(f"{BASE_DIR}{dataset}")

        DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
        result = dict.fromkeys(DAYS)

        # Choose best fitting location type
        order = ("park", "restaurant", "supermarket", "store") # Store default case when no match
        determinant = {
            # Types that map to park
            "park": "park",
            # Types that map to restaurant
            "food": "restuarant",
            "restaurant": "restaurant",
            # Types that map to supermarket
            "supermarket": "supermarket",
            # Types that map to store
            "store": "store",
            "establishment": "store"
        }
        location_type = None
        INACCURATE_FLAG = False
        for item in order:
            # Search by priority for first matching type
            if item in location_types:
                location_type = item
                break
        if not location_type:
            # Try searching by location type next
            for item in location_types:
                if item in determinant:
                    location_type = determinant[item]
                    break
            INACCURATE_FLAG = True
            location_type = "store" # default case

        # Read simulated data
        path = BASE_DIR + valid_location_types[location_type]
        with open(path) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=",")
            for row in csvreader:
                try:
                    if row[0] not in DAYS:
                        raise TypeError(f"malformed {path}")
                    result[row[0]] = list(map(int, row[1:]))
                except ValueError:
                    raise TypeError(f"malformed {path}")

        return result, INACCURATE_FLAG
