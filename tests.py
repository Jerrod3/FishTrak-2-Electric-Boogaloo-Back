import unittest
import requests

HOST = "http://127.0.0.1:8000"  # for local development and testing


class FishermanTests(unittest.TestCase):
    path = 'fishermen'
    ids = []

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
            res: requests.Response = post_data(cls.path, fisherman)
            cls.ids.append(res.json().get('_id'))

    def test_catch_fish(self):
        # need to add backend logic for adding a species to a fisherman's caught_species array
        # https://www.mongodb.com/docs/manual/reference/operator/update/addToSet/
        # not sure of the best way to handle this
        pass

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
        self.ids.remove(_id)
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

    @classmethod
    def setUpClass(cls) -> None:
        # make two post requests to give the tests some data to work with
        body_1 = {
            "name": "St. Mary's Lake",
            "is_freshwater": True,
            "is_stocked": False,
            "location": (42.378229, -85.181098)
        }
        body_2 = {
            "name": "Kzoo River",
            "is_freshwater": True,
            "is_stocked": True
        }
        for body in [body_1, body_2]:
            post_data('bodies', body)

    def test_put(self):
        _id, _ = find_id_by_param('name', "Kzoo River", 'bodies')
        res = requests.get(f"{HOST}/bodies/{_id}")

        requests.put(f"{HOST}/bodies/{_id}", json={"is_stocked": False})
        requests.put(f"{HOST}/bodies/{_id}", json={"location": (42.349159, 85.268510)})
        self.assertEqual(200, res.status_code)

        res = requests.get(f"{HOST}/bodies/{_id}")
        self.assertEqual(200, res.status_code)

        # test for a 3 dimensional location to be rejected
        res = requests.put(f"{HOST}/bodies/{_id}", json={"location": (42.3, 85.2, 36)})
        self.assertEqual(400, res.status_code)

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

    def test_delete(self):
        _id, _ = find_id_by_param('name', "St. Mary's Lake", 'bodies')
        res = requests.delete(f"{HOST}/bodies/{_id}")
        self.assertEqual(204, res.status_code)
        with self.assertRaises(IDNotFoundError):
            find_id_by_param('name', "St. Mary's Lake", 'bodies')

    @classmethod
    def tearDownClass(cls) -> None:
        _id, _ = find_id_by_param('name', 'Kzoo River', 'bodies')
        requests.delete(f"{HOST}/bodies/{_id}")


class SpeciesTest(unittest.TestCase):
    path = 'species'
    ids = []

    @classmethod
    def setUpClass(cls) -> None:
        species_1 = {
            "name": "River Trout",
            "description": "A happy little river trout"
        }
        species_2 = {
            "name": "Striped Bass",
        }
        for species in [species_1, species_2]:
            res = post_data(cls.path, species)
            cls.ids.append(res.json().get('_id'))

    def test_get_all(self):
        res = requests.get(f"{HOST}/{self.path}")
        self.assertEqual(200, res.status_code)

    def test_post(self):
        species = {
            "name": "Brown Trout",
            "description": "A happy little brown trout"
        }

        # post the new species
        res: requests.Response = requests.post(f"{HOST}/{self.path}", json=species)
        _id = res.json().get('_id')
        self.ids.append(_id)
        self.assertEqual(201, res.status_code)

        # ensure it is in the db
        res: requests.Response = requests.get(f"{HOST}/{self.path}/{_id}")
        self.assertEqual(200, res.status_code)
        self.assertTrue(res.json().get('name'), 'Brown Trout')

    @classmethod
    def tearDownClass(cls) -> None:
        for _id in cls.ids:
            requests.delete(f"{HOST}/{cls.path}/{_id}")


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
        raise IDNotFoundError(f"No matching {route.title()} was found")

    return found_item.get('_id'), res.status_code


class IDNotFoundError(Exception):
    pass


if __name__ == '__main__':
    unittest.main()
