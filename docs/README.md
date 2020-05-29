# Soteria
Bryan Carl (bc), Morgan Edlund (me), Daniel Leef (dl), Jinhu Qi (jq), and Carter Perkins (cp)
Group 2

Created: 25 May 2020
Modified: 25 May 2020 (cp)

A web-based, smart planning application.

CIS 422 - Project 2
Soteria was created to assist in the mitigation of overcrowded business and public spaces in the wake of COVID-19. As Soteria is not officially hosted, personal user data is not transmitted to a remote server and geospatial location information is only stored on the client. Through smart scheduling and optimization algorithms, Soteria simultaneously helps users achieve their necessary mental and phyiscal health needs, while reducing the spread of COVID-19.

## Dependencies
* Python 3(Specific Version?)
* Modern Web Browser (Google Chrome, Mozilla Firefox, Safari, Microsoft Edge)
* git (Optional. For building directly from the GitHub repository.)

## Installation

1. Clone the repository

`git clone https://github.com/bryancarl7/project2-soteria.git`

2. Place the `credentials.ini` in the root directory of the cloned project repository. This file is provided directly by the Soteria team.

3. Install the application

`./alphaBuild` (change name & add mechanism to verify port use?)

## Usage

After installation, the user can access the web page via the following URL:
<http://127.0.0.1:PORT> where PORT is the number displayed after running `./alphaBuild` in step 2 of the installation.

## Testing Framework

The testing framework can be executed at anytime, by running `python3 -m test.test` (switch to script?).

## Directory Structure
* populartimes/ - Local installation of the the populartimes package
* data/
    * busy_times/
        * simulated_data/
            * food.csv
            * grocery.csv
            * parks.csv
            * store.csv
        * manager.py
        * reporter.py
    * apiHandler.py
    * bestPlace.py
    * bestTime.py
    * scheduler.py
* docs/
    * README.md
    * resources.md
* server/
    * static/
        * css/
            * img/
                * schedule.jpg
                * times.jpg
            * index.css
            * soteria.css
        * js/
            * soteria.js
    * templates/
        * index.html
        * scheduler.html
        * soteria.html
        * times.html
    * api.py
* test/
    * _\_init_\_.py
    * test.py
* tmp/
    * soteria.log
* alphaBuild - Installation script
* credentials.ini - API keys, must be manually provided and set
* _\_init_\_.py - Python modular structure
* requirements.txt - Python third party packages
* README.md - This file
