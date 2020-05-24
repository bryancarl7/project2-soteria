"""
manager.py

===============================================================================

Last Modified: 23 May 2020
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
    def get_busy_times(cls, location_type):
        """
        Returns the simulated busy time interval for a location type.

        Arguments:
            location_type   (String)        - Location Type
        Returns:
            Dictionary                      - Busy Time Intervals
                Key         (String)        - Day of the Week
                Value       (Int List)      - Hour Occupancy Ratios
        Raises:
            ValueError                      - location_type invalid
            FileNotFoundError               - Missing simulated data file(s)
        """

        # https://developers.google.com/places/supported_types
        # TODO: Smart type to simulated filter
        valid_location_types = {"restaurant": cls.files[0],
                                "store": cls.files[3],
                                "supermarket": cls.files[1],
                                "park": cls.files[2]}

        # Validate input
        if location_type not in valid_location_types:
            raise ValueError("argument 'location_type' is invalid")

        BASE_DIR = os.path.dirname(os.path.realpath(__file__))
        for dataset in cls.files:
            if not os.path.isfile(f"{BASE_DIR}{dataset}"):
                raise FileNotFoundError(f"{BASE_DIR}{dataset}")

        DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
        result = dict.fromkeys(DAYS)

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

        return result
