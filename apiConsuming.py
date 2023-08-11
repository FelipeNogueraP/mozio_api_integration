"""The class and methods used for consuming the Mozio Api"""

import requests
import time
import json


class MozioApi:
    # Class for consuming Mozio API
    BASE_URL = 'https://api-testing.mozio.com'
    HEADERS = {
        'API-KEY': '6bd1e15ab9e94bb190074b4209e6b6f9',
        'Content-Type': 'application/json'
    }

    @classmethod
    def search(cls, params):
        # Method to create search and get initial info.
        endpoint = f'{cls.BASE_URL}/v2/search/'
        response = requests.post(endpoint, headers=cls.HEADERS, json=params)
        return response.json()

    @classmethod
    def poll_search(cls, search_id):
        # Method to iterates in the results until 'more_coming' became False
        endpoint = f'{cls.BASE_URL}/v2/search/{search_id}/poll/'

        all_responses = []

        while True:
            response = requests.get(endpoint, headers=cls.HEADERS)
            response_data = response.json()

            all_responses.append(response_data)

            # Pull until more_coming comes False
            if not response_data.get('more_coming', True):
                break

            # Waits two secconds before pull again
            time.sleep(2)

        with open('poll_search_results.json', 'w') as file:
            json.dump(all_responses, file, indent=4)

        return all_responses

    @classmethod
    def get_cheapest_dummy_provider(cls, poll_responses):
        # Filter by provider name and by price

        dummy_providers = []

        # Iterate over each poll response
        for response in poll_responses:
            results = response.get('results', [])
            dummy_providers.extend([result for result in results if result['steps']
                                   [0]['details']['provider']['name'] == 'Dummy External Provider'])

        if not dummy_providers:
            print("No dummy provider found in the poll response.")
            return None

        # Sort by price and return the lowest one
        cheapest_dummy = sorted(dummy_providers, key=lambda x: float(
            x['total_price']['total_price']['value']))[0]
        return cheapest_dummy

    @classmethod
    def book_reservation(cls, poll_responses):
        # Booking reservation with given data from poll result,
        # and the lowest price service from dummy provider.

        # Extract the cheapest dummy provider
        cheapest_dummy = cls.get_cheapest_dummy_provider(poll_responses)

        if not cheapest_dummy:
            return None

        # Extract the required ids from the cheapest dummy
        search_id = cheapest_dummy.get('search_id')
        result_id = cheapest_dummy.get('result_id')

        # Prepare booking payload
        booking_payload = {
            "search_id": poll_responses[0].get("search_id"),
            "result_id": cheapest_dummy.get("result_id"),
            "email": "test@email.com",
            "country_code_name": "US",
            "phone_number": "8776665544",
            "first_name": "Felipe",
            "last_name": "Noguera",
            "airline": "AA",
            "flight_number": "5555"
        }

        # Making the booking request
        endpoint = f'{cls.BASE_URL}/v2/reservations/'
        response = requests.post(
            endpoint, headers=cls.HEADERS, json=booking_payload)

        return response.json()


if __name__ == '__main__':
    search_params = {
        'start_address': '44 Tehama Street, San Francisco, CA, USA',
        'end_address': 'SFO',
        'mode': 'one_way',
        'pickup_datetime': '2023-12-01 15:30',
        'num_passengers': 2,
        'currency': 'USD',
        'campaign': 'Felipe Noguera'
    }

    # Test Search method
    search_response = MozioApi.search(search_params)
    # print('search_response: ', search_response)
    print('search_response: succesfull')

    # Test poll_search method
    search_id = search_response['search_id']
    poll_response = MozioApi.poll_search(search_id)
    print('poll_response: succesfull')

    # Test book_reservation method
    booking_response = MozioApi.book_reservation(poll_response)
    print(booking_response)
    print("booking succesfull")
