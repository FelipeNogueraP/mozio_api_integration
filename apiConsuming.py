"""The class and methods used for consuming the Mozio Api"""

import requests
import time


class MozioApi:
    # Class for consuming Mozio API
    BASE_URL = 'https://api-testing.mozio.com'
    HEADERS = {
        'API-KEY': '6bd1e15ab9e94bb190074b4209e6b6f9',
        'Content-Type': "application/json"
    }

    @classmethod
    def search(cls, params):
        # Method to create search and get initial info.
        endpoint = f"{cls.BASE_URL}/v2/search/"
        response = requests.post(endpoint, headers=cls.HEADERS, json=params)
        return response.json()

    @classmethod
    def poll_search(cls, search_id):
        # Method to iterates in the results until "more_coming" became False
        endpoint = f"{cls.BASE_URL}/v2/search/{search_id}/poll/"

        while True:
            response = requests.get(endpoint, headers=cls.HEADERS)
            response_data = response.json()

            # Pull until more_coming comes False
            if not response_data.get('more_coming', True):
                return response_data

            # Waits two secconds before pull again
            time.sleep(2)


if __name__ == "__main__":
    search_params = {
        "start_address": "44 Tehama Street, San Francisco, CA, USA",
        "end_address": "SFO",
        "mode": "one_way",
        "pickup_datetime": "2023-12-01 15:30",
        "num_passengers": 2,
        "currency": "USD",
        "campaign": "Felipe Noguera"
    }

    # Test Search method
    search_response = MozioApi.search(search_params)
    print('search_response: ', search_response)

    # Test poll_search method
    search_id = search_response['search_id']
    poll_response = MozioApi.poll_search(search_id)
    print('poll_response: ', poll_response)
