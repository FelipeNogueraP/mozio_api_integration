import unittest
from unittest import mock
from apiConsuming import MozioApi


class TestMozioApi(unittest.TestCase):

    def test_search(self):
        with mock.patch('requests.post') as mock_post:
            mock_post.return_value.json.return_value = {"search_id": "123456"}
            mock_post.return_value.status_code = 200

            response = MozioApi.search({})
            self.assertEqual(response, {"search_id": "123456"})

    def test_poll_search(self):
        with mock.patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = {
                "more_coming": False, "results": []}
            mock_get.return_value.status_code = 200

            response = MozioApi.poll_search("123456")
            self.assertEqual(response[-1]['more_coming'], False)

    def test_get_cheapest_dummy_provider(self):
        poll_responses = [{
            "results": [{
                "search_id": "123456",
                "result_id": "78910",
                "total_price": {"total_price": {"value": "100"}},
                "steps": [{
                    "details": {
                        "provider": {
                            "name": "Dummy External Provider"
                        }
                    }
                }]
            },
                {
                "search_id": "654321",
                "result_id": "101112",
                "total_price": {"total_price": {"value": "50"}},
                "steps": [{
                    "details": {
                        "provider": {
                            "name": "Another Provider"
                        }
                    }
                }]
            }]
        }]
        cheapest = MozioApi.get_cheapest_dummy_provider(poll_responses)
        self.assertEqual(cheapest["result_id"], "78910")

    def test_book_reservation(self):
        with mock.patch('requests.post') as mock_post:
            mock_post.return_value.json.return_value = {
                "confirmation_number": "123456"}
            mock_post.return_value.status_code = 200

            response = MozioApi.book_reservation([{
                "results": [{
                    "search_id": "123456",
                    "result_id": "78910",
                    "total_price": {"total_price": {"value": "100"}},
                    "steps": [{
                        "details": {
                            "provider": {
                                "name": "Dummy External Provider"
                            }
                        }
                    }]
                }]
            }])

            self.assertIn('confirmation_number', response)

    def test_poll_reservation(self):
        with mock.patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = {"status": "completed"}
            mock_get.return_value.status_code = 200

            response = MozioApi.poll_reservation("123456")
            self.assertEqual(response["status"], "completed")

    def test_cancel_reservation(self):
        with mock.patch('requests.delete') as mock_delete:
            mock_delete.return_value.json.return_value = {
                "cancelled": 1, "refunded": 1}
            mock_delete.return_value.status_code = 202

            response = MozioApi.cancel_reservation("123456")
            self.assertEqual(response, {"cancelled": 1, "refunded": 1})


if __name__ == "__main__":
    unittest.main()
