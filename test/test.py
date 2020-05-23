import unittest
import requests
from server.api import app, api, PORT, ENV, HOST, apiHandler
from data.bestTime import bestTime
from data.bestPlace import bestPlace
from data.scheduler import scheduler

class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("test start\n")
        # app.run(HOST, PORT, debug=True)
        # api.add_resource(bestTime, "/times/bestTime")
        # api.add_resource(bestPlace, "/times/bestPlace")
        # api.add_resource(scheduler, "/scheduler/update")

    @classmethod
    def test_something(cls):
        response = requests.get("http://localhost:3000/")
        assert(response.status_code, 200)

    def test_bestTime(self):
        bT = bestTime(apiHandler)
        parsed = bT.make_request()
        self.assertIsNotNone(parsed)

    def test_bestPlace(self):
        bP = bestPlace(apiHandler)
        parsed = bP.make_request()
        self.assertIsNotNone(parsed)

    @classmethod
    def test_apiBestPlace(cls):
        response_place = requests.get("http://0.0.0.0:3000/times/bestPlace")
        assert(response_place.status_code, 200)
        print("best place page successfully created")


    @classmethod
    def test_apiBestTime(cls):
        response_time = requests.get("http://0.0.0.0:3000/times/bestTime")
        assert(response_time.status_code, 200)
        print("best time page successfully created")


    @classmethod
    def test_apiBestScheduler(cls):
        response_scheduler = requests.get("http://0.0.0.0:3000/scheduler/update")
        assert(response_scheduler.status_code, 200)
        print("scheduler page successfully created")

    def tearDown(self):
        print("test end")

if __name__ == '__main__':
    unittest.main()
