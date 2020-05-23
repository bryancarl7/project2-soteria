"""
manager.py

===============================================================================

Last Modified: 22 May 2020
Modification By: Carter Perkins

Creation Date: 22 May 2020
Initial Author: Carter Perkins

===============================================================================

This is a submodule of the Busy Times Reporter that handles interactions with
the simulated data. Although independent, this component should only interface
with the driver of the larger module found in 'reporter.py'.
"""

# Standard Import
import csv
import os

class SimulationManager():
    """
    The SimulationManager class is the interface for reading simulated data.
    """

    # Setup data file paths
    path = "data/busy_times/simulated_data/"
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

        valid_location_types = ("temporary": cls.files[0])

        # Validate input
        if location_type not in valid_location_types:
            raise ValueError("argument 'location_type' is invalid")

        # Verify files exist
        for f in files:
            if not os.path.isfile(f):
                raise FileNotFoundError(f)

        DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                "Saturday", "Sunday")
        result = dict.fromkeys(DAYS)
        with open(cls.files[location_type]) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=",")
            for row in csvreader:
                try:
                    if row[0] not in DAYS:
                        raise TypeError(f"malformed {cls.files[location_type]}")
                    result[row[0]] = list(map(int, row[1:]))
                except ValueError:
                    raise TypeError(f"malformed {cls.files[location_type]}")

        return result
