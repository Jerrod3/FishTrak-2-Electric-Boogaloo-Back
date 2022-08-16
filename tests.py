import unittest
import requests
from main import my_func
from models import Fisherman

HOST = "http://127.0.0.1:8000"  # for local development and testing


class BasicTests(unittest.TestCase):

    def test1(self):
        expected = "Hello World"
        self.assertEqual(my_func(), expected)

    def test2(self):
        expected = "Goodbye World"
        self.assertNotEqual(my_func(), expected)

    def test_root_route(self):
        expected = {"msg": "Hello, world!"}
        res = requests.get(HOST)
        data = res.json()
        self.assertIsInstance(data, dict)
        self.assertEqual(data, expected)


class FishermanTests(unittest.TestCase):

    def test_post(self):
        fisherman = Fisherman(first="Jerrod", last="Lepper")
        res = requests.post(f"{HOST}/fishermen", json=fisherman.dict())
        # a successful request sends back the same data as a response
        self.assertEqual(res.json(), fisherman.dict())

    def test_get_all(self):
        fishermen = requests.get(f"{HOST}/fishermen")
        self.assertIsInstance(fishermen.json(), list)


if __name__ == '__main__':
    unittest.main()
