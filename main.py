"""Run this file to get the API calls. 
    Main file in the application"""

from apiConsuming import MozioApi
import time

search_params = {
    'start_address': '44 Tehama Street, San Francisco, CA, USA',
    'end_address': 'SFO',
    'mode': 'one_way',
    'pickup_datetime': '2023-12-01 15:30',
    'num_passengers': 2,
    'currency': 'USD',
    'campaign': 'Felipe Noguera'
}


if __name__ == '__main__':

    # Start Search
    search_response = MozioApi.search(search_params)

    # Test poll_search method
    search_id = search_response['search_id']
    poll_response = MozioApi.poll_search(search_id)
    print("Looking for the cheapest option in the Dummy provider")

    # Test book_reservation method
    booking_response = MozioApi.book_reservation(poll_response)
    if booking_response:
        final_response = poll_response[-1]
        search_id = final_response.get('search_id')
    print("Reservation in progress")

    # Test poll_reservation
    reservation_poll_response = MozioApi.poll_reservation(search_id)
    # get the reservation id
    if reservation_poll_response['reservations']:
        reservation_id = reservation_poll_response['reservations'][0]['id']
        print(
            f"The booking has been succesfully and the reservation number is {reservation_id}")
    else:
        print("No reservations found in the poll response.")
        reservation_id = None

    time.sleep(2)
    # Cancel reservation
    cancellation_result = MozioApi.cancel_reservation(reservation_id)
    print(
        f"Reservation No. {reservation_id} with status: canceled ", cancellation_result)
