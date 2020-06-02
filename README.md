# Soteria
Bryan Carl (bc), Morgan Edlund (me), Daniel Leef (dl), Jinhu Qi (jq), and Carter Perkins (cp)
Group 2

Created: 25 May 2020
Modified: 1 June 2020 (cp)

A web-based, smart planning application.

CIS 422 - Project 2
Soteria was created to assist in the mitigation of overcrowded business and public spaces in the wake of COVID-19. As Soteria is not officially hosted, personal user data is not transmitted to a remote server and geospatial location information is only stored on the client. Through smart scheduling and optimization algorithms, Soteria simultaneously helps users achieve their necessary mental and phyiscal health needs, while reducing the spread of COVID-19.

## Dependencies
* Python 3.6
* Modern Web Browser* (Google Chrome, Safari)
* git

*Note: Mozilla Firefox has been noted to have a few issues properly displaying CSS so it is recommended to use one of the listed browsers. Other browsers are untested.

## Installation

1. Clone the repository

`git clone https://github.com/bryancarl7/project2-soteria.git`

2. Place the `credentials.ini` in the root directory of the cloned project repository. This file is provided directly by the Soteria team.

3. Install the application

Run `./build.sh` using your favorite Bash supported terminal

_NOTE_: There were multithreading issues on Mac OS X during development, we reflected this in our build<br>
scripts, however if you run into issue you may have to run command this to allow multithreading: <br>

`export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`

Run this command in terminal and restart afterwards and the multithreading issue should subside. <br>
Source: `https://stackoverflow.com/questions/50168647/multiprocessing-causes-python-to-crash-and-gives-an-error-may-have-been-in-progr`

## Usage

After installation, the user can access the web page via the following URL:
<http://127.0.0.1:PORT> where PORT is the number displayed after running the build script in step 2 of the installation. 

Note: if your machine is exposed to the internet the URL may be <http://MY_SYSTEM_URL:PORT>

## Testing Framework

The testing framework can be executed at anytime, by running `python3 -m test.test`. Note: this tests every function in the project which can take a couple of minutes to complete.

## Directory Structure
* data/ - Contains the Popular Place Data Processor and Busy Times Reporter Modules
    * busy_times/ - Root Directory for Busy Times Reporter
        * simulated_data/ - Contains the Simulated Datasets
            * food.csv - Simulated Dataset for Food Types
            * grocery.csv - Simulated Dataset for Grocery Types
            * parks.csv - Simulated Dataset for Park Types
            * store.csv - Simulated Datasets for Store Types
        * manager.py - Simulation Manager for the Busy Times Reporter
        * reporter.py - Main Interface for the Busy Times Reporter
    * apiHandler.py
    * bestPlace.py
    * bestTime.py
    * scheduler.py
* docs/ - Documents related to overall system
    * resources.md - External resources for implementing project
* server/ - Contains the Popular Places Interface and Server
    * static/ - Static files for the Popular Places Interface
        * css/ - CSS File Directory
            * img/ - Image File Directory
                * schedule.jpg - Schedule Image
                * times.jpg - Times Image
            * index.css - Index CSS File
            * soteria.css - Soteria CSS File
        * js/ - Javascript Directory
            * soteria.js - Soteria JS File
    * templates/ - Directory for Web Pages
        * index.html - Index Web Page
        * scheduler.html - Scheduler Web Page
        * soteria.html - Soteria Web Page
        * times.html - Times Web Page
    * api.py - Main Interface for Flask API 
* test/ - Testing Framework Directory
    * _\_init_\_.py - Allows directory to be run as a module
    * test.py - Main Testing Framework Interface
* tmp/ - Temporary Directory for Logs
    * soteria.log - Main Log File
* builds/ - Directory for OS Depdendent Build Scripts
    * build_linux - Installation script for Linux/MacOS platforms
    * build_windows.sh - Installation script for Windows platfomrs
* build.sh - Main Interface for Installing
* credentials.ini - API keys, must be manually provided and set
* _\_init_\_.py - Python modular structure
* requirements.txt - Python third party packages
* README.md - This file
