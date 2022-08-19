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
        res = requests.get(f"{HOST}/fishermen")
        self.assertEqual(200, res.status_code)
        self.assertIsInstance(res.json(), list)

    def test_get_by_id(self):
        _id, code = find_id_by_email('ljensen@tobi.dog', 'fishermen')
        self.assertEqual(200, code)
        res = requests.get(f"{HOST}/fishermen/{_id}")
        self.assertEqual(200, res.status_code)
        name = f"{res.json().get('first')} {res.json().get('last')}"
        self.assertEqual("Lucas Jensen", name)

    def test_delete(self):
        _id, code = find_id_by_email('jlepper@basil.dog', 'fishermen')
        self.assertEqual(200, code)
        res = requests.delete(f"{HOST}/fishermen/{_id}")
        self.assertEqual(204, res.status_code)

    def test_put(self):
        _id, _ = find_id_by_email('ljensen@tobi.dog', 'fishermen')
        res = requests.put(f"{HOST}/fishermen/{_id}", json={'first': 'Lucas Paul'})
        self.assertEqual("Lucas Paul Jensen", f"{res.json().get('first')} {res.json().get('last')}")

    @classmethod
    def tearDownClass(cls) -> None:
        # the above tests should only leave Lucas Jensen in the fishermen collection
        # It should be removed to restore the db to its pre-test state
        _id, _ = find_id_by_email('ljensen@tobi.dog', 'fishermen')
        requests.delete(f"{HOST}/fishermen/{_id}")


def post_data(route: str, data: dict) -> requests.Response:
    res = requests.post(f"{HOST}/{route}", json=data)
    return res


def find_id_by_email(email: str, route: str) -> tuple[str, int]:
    # first get all data to find the desired _id
    res = requests.get(f"{HOST}/{route}")

    found_entity = None
    data = res.json()
    for entity in data:
        if entity.get('email') == email:
            found_entity = entity

    if found_entity is None:
        raise Exception(f"No matching {route.title()} was found")

    return found_entity.get('_id'), res.status_code


if __name__ == '__main__':
    unittest.main()
