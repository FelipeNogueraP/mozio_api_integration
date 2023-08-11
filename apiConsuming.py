"""The class and methods used for consuming the Mozio Api"""

import requests
import time
import json
import random


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
            print("Looking for results ...")
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
        # Generate random flight numbers to avoid the error, duplicate_reservation
        flight_num = random.randint(1, 999)

        booking_payload = {
            "search_id": poll_responses[0].get("search_id"),
            "result_id": cheapest_dummy.get("result_id"),
            "email": "test@email.com",
            "country_code_name": "US",
            "phone_number": "8776665544",
            "first_name": "Felipe",
            "last_name": "Noguera",
            "airline": "AA",
            "flight_number": flight_num
        }

        # Making the booking request
        endpoint = f'{cls.BASE_URL}/v2/reservations/'
        response = requests.post(
            endpoint, headers=cls.HEADERS, json=booking_payload)

        return response.json()

    @classmethod
    def poll_reservation(cls, search_id):
        endpoint = f'{cls.BASE_URL}/v2/reservations/{search_id}/poll/'

        while True:
            response = requests.get(endpoint, headers=cls.HEADERS)

            # Check if the response is a JSON
            try:
                response_data = response.json()

            except ValueError:
                print("Received non -json response: ", response.status_code)
                print(response.text)
                response_data = {}

            # Check reservation status. If the "completed" status appears, break the loop.
            if response_data.get('status', '') == 'completed':
                break
            if response_data.get('status', '') == 'failed':
                print('Failed', response.status_code)
                break

            # Waits for a specific time before pulling again.
            time.sleep(2)

        return response_data

    @classmethod
    def cancel_reservation(cls, reservation_id):
        # Cancels an existing reservation.
        endpoint = f"{cls.BASE_URL}/v2/reservations/{reservation_id}/"
        response = requests.delete(endpoint, headers=cls.HEADERS)

        # Check if the request was successful
        if response.status_code == 202:
            return response.json()
        else:
            return {'error': 'Cancelation failed', 'details': response.json()}
