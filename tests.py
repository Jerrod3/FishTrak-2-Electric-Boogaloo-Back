import unittest
import requests
from requests import Response


HOST = "http://127.0.0.1:8000"  # for local development and testing


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
        post_sample(cls.route, [fisherman_1, fisherman_2], cls.ids)

    def test_catch_fish(self):
        # need to add backend logic for adding a species to a fisherman's caught_species array
        # https://www.mongodb.com/docs/manual/reference/operator/update/addToSet/
        # not sure of the best way to handle this
        pass

    def test_post(self):
        fisherman = {"first": "Margarite",
                     "last": "Waddell",
                     "email": "mwaddell@carol.cat"}
        res: Response = post_data(self.route, fisherman)
        _id = res.json().get('_id')
        self.ids.append(_id)
        self.assertEqual(201, res.status_code)
        self.assertEqual(fisherman.get('email'), res.json().get('email'))

        res: Response = requests.get(f"{HOST}/{self.route}/{_id}")
        self.assertEqual(fisherman.get('email'), res.json().get('email'))

    def test_get_all(self):
        res = requests.get(f"{HOST}/{self.route}/")
        self.assertEqual(200, res.status_code)

    def test_get_by_id(self):
        _id, code = find_id_by_param('email', 'ljensen@tobi.dog', self.route)
        self.assertEqual(200, code)
        res = requests.get(f"{HOST}/{self.route}/{_id}")
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
        clear_db(cls.ids, cls.route)


class LureTests(unittest.TestCase):
    route = 'lures'
    ids = []

    @classmethod
    def setUpClass(cls) -> None:
        # make two post requests to give the tests some data to work with
        lure_1 = {
            "name": "Senko",
            "type": "Drop Shot",
            "color": "purple"
        }
        lure_2 = {  # no weight field, as it is optional
            "name": "Daredevil",
            "type": "flying",
            "color": "red"
        }
        post_sample(cls.route, [lure_1, lure_2], cls.ids)

    def test_post(self):
        lure = {  # no color or weight field, as it is optional
            "name": "worm",
            "type": "natural",
        }
        res = post_data(self.route, lure)
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
    route = 'bodies'
    ids = []

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
        post_sample(cls.route, [body_1, body_2], cls.ids)

    def test_put(self):
        _id, _ = find_id_by_param('name', "Kzoo River", 'bodies')
        res = requests.get(f"{HOST}/{self.route}/{_id}")

        requests.put(f"{HOST}/{self.route}/{_id}", json={"is_stocked": False})
        requests.put(f"{HOST}/{self.route}/{_id}", json={"location": (42.349159, 85.268510)})
        self.assertEqual(200, res.status_code)

        res = requests.get(f"{HOST}/{self.route}/{_id}")
        self.assertEqual(200, res.status_code)

        # test for a 3 dimensional location to be rejected
        res = requests.put(f"{HOST}/{self.route}/{_id}", json={"location": (42.3, 85.2, 36)})
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
        self.ids.append(res.json().get('_id'))

    def test_delete(self):
        _id, _ = find_id_by_param('name', "St. Mary's Lake", 'bodies')
        res = requests.delete(f"{HOST}/bodies/{_id}")
        self.ids.remove(_id)
        self.assertEqual(204, res.status_code)
        with self.assertRaises(IDNotFoundError):
            find_id_by_param('name', "St. Mary's Lake", 'bodies')

    @classmethod
    def tearDownClass(cls) -> None:
        clear_db(cls.ids, cls.route)


class SpeciesTest(unittest.TestCase):
    route = 'species'
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
        post_sample(cls.route, [species_1, species_2], cls.ids)

    def test_get_all(self):
        res = requests.get(f"{HOST}/{self.route}")
        self.assertEqual(200, res.status_code)

    def test_post(self):
        species = {
            "name": "Brown Trout",
            "description": "A happy little brown trout"
        }

        # post the new species
        res: requests.Response = requests.post(f"{HOST}/{self.route}/", json=species)
        _id = res.json().get('_id')
        self.ids.append(_id)
        self.assertEqual(201, res.status_code)

        # ensure it is in the db
        res: requests.Response = requests.get(f"{HOST}/{self.route}/{_id}/")
        self.assertEqual(200, res.status_code)
        self.assertTrue(res.json().get('name'), 'Brown Trout')

    @classmethod
    def tearDownClass(cls) -> None:
        clear_db(cls.ids, cls.route)


def post_sample(route: str, data: list[dict], ids: list[str]) -> None:
    for entity in data:
        res: Response = requests.post(f"{HOST}/{route}/", json=entity)
        ids.append(res.json().get('_id'))


def clear_db(ids: list, route: str) -> None:
    for _id in ids:
        requests.delete(f"{HOST}/{route}/{_id}/")


def post_data(route: str, data: dict) -> requests.Response:
    res = requests.post(f"{HOST}/{route}/", json=data)
    return res


def find_id_by_param(param: str, value: str, route: str) -> tuple[str, int]:
    """
    USE WITH CAUTION: may not work as intended with non-unique parameters
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
