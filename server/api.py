from data.bestTime import bestTime
from data.bestPlace import bestPlace
from data.scheduler import scheduler
from flask import Flask, render_template
from flask_restful import Api
import logging

#########################################
# Written by: Bryan Carl May 15, 2020   #
# Group 2: Project Soteria              #
#########################################

# Some environment vars, don't mind me
ENV = 'production'
PORT = input("Please enter a PORT you would like to host on (four digits 0-9): ")
HOST = '0.0.0.0'

# Setup Apps/API
app = Flask(__name__)
api = Api(app)


@app.route("/")
def index():
    return render_template("soteria.html")


# added the api resources to the appropiate
api.add_resource(bestTime, "/times/bestTime")
api.add_resource(bestPlace, "/times/bestPlace")
api.add_resource(scheduler, "/scheduler/update")


if __name__ == "__main__":
    try:
        logging.basicConfig(filename='tmp/soteria.log', level=logging.DEBUG,
                            format="%(asctime)s - %(levelname)s - %(message)s",
                            datefmt="%m/%d/%Y %H:%M:%S %p")
        try:
            # Attempt to run the app
            print("\n\t* Running on http://0.0.0.0:{} *\n".format(PORT))
            print("Unless Hosted on a domain, then replace the '0.0.0.0' with your domain")

            # Run the app and get the successful exit
            app.run(host=HOST, port=PORT, debug=False)
            app.logger.info("Successfully exited app")

        except Exception as ex:
            # unsure whish is being tripped so we have to check
            app.logger.warning("Could not host Flask App")
            app.logger.exception(ex.__traceback__)
    except FileNotFoundError as ex:
        print("Unable to setup logging, please ensure you have ran the build script")