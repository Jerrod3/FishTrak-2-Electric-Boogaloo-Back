import unittest
import requests

HOST = "http://127.0.0.1:8000"  # for local development and testing


class FishermanTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # make two post requests to give the tests some data to work with
        fisherman1 = {"first": "Jerrod",
                      "last": "Lepper",
                      "email": "jlepper@basil.dog"}
        fisherman2 = {"first": "Lucas",
                      "last": "Jensen",
                      "email": "ljensen@tobi.dog"}
        for fisherman in [fisherman1, fisherman2]:
            post_data('fishermen', fisherman)

    def test_post(self):
        fisherman = {"first": "Margarite",
                     "last": "Waddell",
                     "email": "mwaddell@carol.cat"}
        res = post_data("fishermen", fisherman)
        self.assertEqual(201, res.status_code)
        self.assertEqual(fisherman.get('email'), res.json().get('email'))
        _id = res.json().get('_id')

        # everything must have check out, so the new entry will be removed
        res = requests.delete(f"{HOST}/fishermen/{_id}")
        self.assertEqual(204, res.status_code)

    def test_get_all(self):
        # GET
        res = requests.get(f"{HOST}/fishermen/")
        self.assertEqual(200, res.status_code)
        self.assertIsInstance(res.json(), list)

    def test_get_by_id(self):
        _id, code = find_id_by_param('email', 'ljensen@tobi.dog', 'fishermen')
        self.assertEqual(200, code)
        res = requests.get(f"{HOST}/fishermen/{_id}")
        self.assertEqual(200, res.status_code)
        name = f"{res.json().get('first')} {res.json().get('last')}"
        self.assertEqual("Lucas Jensen", name)

    def test_delete(self):
        _id, code = find_id_by_param('email', 'jlepper@basil.dog', 'fishermen')
        self.assertEqual(200, code)
        res = requests.delete(f"{HOST}/fishermen/{_id}")
        self.assertEqual(204, res.status_code)

    def test_put(self):
        _id, _ = find_id_by_param('email', 'ljensen@tobi.dog', 'fishermen')
        res = requests.put(f"{HOST}/fishermen/{_id}", json={'first': 'Lucas Paul'})
        self.assertEqual("Lucas Paul Jensen", f"{res.json().get('first')} {res.json().get('last')}")

    @classmethod
    def tearDownClass(cls) -> None:
        # the above tests should only leave Lucas Jensen in the fishermen collection
        # It should be removed to restore the db to its pre-test state
        _id, _ = find_id_by_param('email', 'ljensen@tobi.dog', 'fishermen')
        requests.delete(f"{HOST}/fishermen/{_id}")


class LureTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # make two post requests to give the tests some data to work with
        lure1 = {
                "name": "Senko",
                "type": "Drop Shot",
                "color": "purple"
            }
        lure2 = {  # no weight field, as it is optional
                "name": "Daredevil",
                "type": "flying",
                "color": "red"
            }
        for lure in [lure1, lure2]:
            post_data('lures', lure)

    def test_post(self):
        lure = {  # no color or weight field, as it is optional
                "name": "worm",
                "type": "natural",
            }
        res = post_data('lures', lure)
        self.assertEqual(201, res.status_code)
        self.assertEqual(lure.get('name'), res.json().get('name'))
        _id = res.json().get('_id')

        # everything must have check out, so the new entry will be removed
        res = requests.delete(f"{HOST}/lures/{_id}")
        self.assertEqual(204, res.status_code)

    def test_get_all(self):
        # GET
        res = requests.get(f"{HOST}/lures/")
        self.assertEqual(200, res.status_code)
        self.assertIsInstance(res.json(), list)

    def test_get_by_id(self):
        _id, code = find_id_by_param('name', 'Senko', 'lures')
        self.assertEqual(200, code)
        res = requests.get(f"{HOST}/lures/{_id}")
        self.assertEqual(200, res.status_code)
        name = f"{res.json().get('name')}"
        self.assertEqual("Senko", name)

    def test_delete(self):
        _id, code = find_id_by_param('name', 'Daredevil', 'lures')
        self.assertEqual(200, code)
        res = requests.delete(f"{HOST}/lures/{_id}")
        self.assertEqual(204, res.status_code)

    def test_put(self):
        _id, _ = find_id_by_param('name', 'Senko', 'lures')
        lure = requests.get(f"{HOST}/lures/{_id}").json()
        self.assertEqual('purple', lure.get('color'))
        self.assertIsNone(lure.get('weight'))

        requests.put(f"{HOST}/lures/{_id}", json={"color": "white", "weight": 1.2})

        lure = requests.get(f"{HOST}/lures/{_id}").json()
        self.assertEqual('white', lure.get('color'))
        self.assertEqual(1.2, lure.get('weight'))

    @classmethod
    def tearDownClass(cls) -> None:
        _id, _ = find_id_by_param('name', 'Senko', 'lures')
        requests.delete(f"{HOST}/lures/{_id}")


class WaterBodiesTest(unittest.TestCase):

    def test_post(self):
        body = {
            "name": "Gull Lake",
            "is_freshwater": True,
            "is_stocked": False,
            "location": (73.856077, 40.848447)
        }
        res = requests.post(f"{HOST}/bodies/", json=body)
        self.assertEqual(201, res.status_code)

        _id = res.json().get('_id')

        res = requests.delete(f"{HOST}/bodies/{_id}")
        self.assertEqual(204, res.status_code)


def post_data(route: str, data: dict) -> requests.Response:
    res = requests.post(f"{HOST}/{route}/", json=data)
    return res


def find_id_by_param(param: str, value: str, route: str) -> tuple[str, int]:
    """
    Finds and returns the first item in a collection that matches the provided parameter
    Also returns the status code of the request. Values are returned as tuple.
    """
    res = requests.get(f"{HOST}/{route}/")
    found_item = None
    data: list = res.json()
    for item in data:
        if item.get(param) == value:
            found_item = item
            break

    if found_item is None:
        raise Exception(f"No matching {route.title()} was found")

    return found_item.get('_id'), res.status_code


if __name__ == '__main__':
    unittest.main()
