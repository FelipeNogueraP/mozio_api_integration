"""The class and methods used for consuming the Mozio Api"""

import requests


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
    print('search_response', search_response)
