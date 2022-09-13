import unittest
from fastapi.testclient import TestClient
from main import app, startup_db_client, shutdown_db_client

client = TestClient(app)


class RootRouteTest(unittest.TestCase):
    def test_root(self):
        res = client.get('/')
        self.assertIsInstance(res.json(), dict)
        self.assertEqual(200, res.status_code)


class FishermanTests(unittest.TestCase):
    route = 'fishermen'
    ids = []

    @classmethod
    def setUpClass(cls) -> None:
        # make two post requests to give the tests some data to work with
        fisherman_1 = {"first": "Jerrod",
                       "last": "Lepper",
                       "email": "jlepper@basil.dog"}
        fisherman_2 = {"first": "Lucas",
                       "last": "Jensen",
                       "email": "ljensen@tobi.dog"}
        fishermen = [fisherman_1, fisherman_2]

        for fisherman in fishermen:
            res = client.post(f'/{cls.route}/', json=fisherman)
            cls.ids.append(res.json()['_id'])

    def test_get_all(self):
        res = client.get(f"/{self.route}/")
        self.assertEqual(200, res.status_code)

    @classmethod
    def tearDownClass(cls) -> None:
        for _id in cls.ids:
            client.delete(f'/{cls.route}/{_id}')


if __name__ == '__main__':
    startup_db_client()
    unittest.main()
    shutdown_db_client()
