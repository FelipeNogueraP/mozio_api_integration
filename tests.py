import unittest
from unittest.mock import patch, Mock


class TestMozioApi(unittest.TestCase):

    # Search Test
    def test_search_successfull(self):
        with patch('request.post') as mock_post:
            mock_response = Mock()
            mock_response.json.return_value = {
                'id': '12345',
                'data': [{'name': 'Dummy External Provider', 'vehicles': []}]
            }
            mock_post.return_value = mock_response

            response = MozioApi.search(search_params)

            self.assertIn('id', response)
            self.assertIn('data', response)
            self.assertTrue(
                any(item['name'] == 'Dummy External Provider' for item in response['data']))

    # Reservation Test

    def test_do_reservation(self):
        with patch('request.post') as mock_post:
            mock_response = Mock()
            mock_response.json.return_value = {
                'confirmation_number': 'ABC123'
            }
            mock_post.return_value = mock_response

            reservation_params = {
                'search_id': '12345',
                'vehicle_id': '6789'
            }
            response = MozioApi.do_reservation(reservation_params)

            self.assertIn('confirmation_number', response)

    # Cancelation test 
    def test_cancel_reservation(self):
        with patch('request.delete') as mock_delete:
            mock_response = Mock()
            mock_response.status_code = 204
            mock_delete.return_value = mock_response

            status = MozioApi.cancel_reservation('ABC123')

            self.assertEqual(status, 204)