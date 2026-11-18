from config import BOOKER_BASE_URL
from clients.booking_client import BookingClient
client = BookingClient(BOOKER_BASE_URL)


def test_get_bookings_returns_list():
    response = client.get_bookings()
    assert response.status_code == 200
    assert isinstance(response.json(), list)