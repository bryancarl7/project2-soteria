import unittest
import requests
from server.api import app, PORT, ENV, HOST, apiHandler


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.run(HOST, PORT, debug=True)

    @classmethod
    def test_something(cls):
        response = requests.get("http://localhost:3000/")
        assert(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
