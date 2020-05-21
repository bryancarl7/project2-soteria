from data.apiHandler import apiHandler
from data.bestTime import bestTime
from data.bestPlace import bestPlace
from data.scheduler import scheduler
from flask import Flask, request, abort, render_template
from flask_restful import Resource, Api

#############################################
# Written by: Bryan Carl May 15, 2020
# Group 2: Project Soteria
#############################################

# Some environment vars, don't mind me
ENV = 'develop'
PORT = 3000
HOST = '0.0.0.0'
HANDLER = apiHandler(PORT, HOST, ENV, "credentials.json")

# Setup Apps/API
app = Flask(__name__)
api = Api(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scheduler")
def schedule():
    return render_template("scheduler.html")


@app.route("/times")
def times():
    return render_template("times.html")


api.add_resource(bestTime, "/times/bestTime")
api.add_resource(bestPlace, "/times/bestPlace")
api.add_resource(scheduler, "/scheduler/update")


if __name__ == "__main__":
    try:
        # Attempt to run the app
        print("Hosting Flask app on Port: " + str(PORT))

        # Run the app and get the successful exit
        app.run(host=HOST, port=PORT, debug=False)
        app.logger.info("Successfully exited app")

    except Exception as ex:
        # unsure whish is being tripped so we have to check
        app.logger.warning("Could not host Flask App")
        app.logger.exception(ex.__traceback__)