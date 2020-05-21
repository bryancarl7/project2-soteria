"""
reporter.py

===============================================================================

Last Modified: 21 May 2020
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

# Standard Imports
import configparser
import enum
import os

class BusyTimesReporter():
    """
    The BusyTimesReporter class serves as the interface for accessing location
    relative occupancy data. The preferred mode, accurate or simulated, can be
    passed at runtime (default simulated).
    """

    # Enum class to determine fetching mode
    class Mode(enum.Enum):
        SIMULATED = 0
        ACCURATE = 1

        @classmethod
        def has_value(cls, value):
            return value in cls._value2member_map_

    def get_api_key():
        """
        Returns the Google Maps API Key as specified in the 'credentials.ini'
        file (see README.md for more details).

        Ideally, this function would be private as the API_KEY should not be
        accessed outside of internal use of this interface.

        Returns:
            String              - Google Maps API Key
        Raises:
            FileNotFoundError   - Missing 'credentials.ini' file
            TypeError           - Malformed 'credentials.ini'
        """

        config = configparser.ConfigParser()

        # Cannot find credentials.ini file, raise error
        if not os.path.isfile("credentials.ini"):
            raise FileNotFoundError("credentials.ini")

        # Read from credentials.ini (root directory)
        config.read("credentials.ini")
        API_KEY = None
        try:
            API_KEY = config.get("DEFAULT", "GoogleMapsAPIKey")
        except (configparser.NoOptionError, KeyError) as e:
            # Invalid credentials.ini
            raise TypeError("malformed 'credentials.ini'")

        return API_KEY

    @classmethod
    def get_busy_times(cls, location, mode):
        """
        Returns an interval representing the busy times of a location.
        """

        # Validate inputs
        if not isinstance(mode, int) and not isinstance(mode, cls.Mode):
            raise TypeError("argument 'mode' must be of type int or BusyTimesReporter.Mode")
        if isinstance(mode, int) and not cls.Mode.has_value(mode):
            raise TypeError("argument 'mode' is invalid")

        # Fetch API Key for accurate mode
        API_KEY = get_api_key()


