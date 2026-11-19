import pytest
from config import BOOKER_BASE_URL, BOOKER_USERNAME, BOOKER_PASSWORD
from clients.booking_client import BookingClient
from data.bookings import valid_booking


@pytest.fixture(scope="session")
def client():
    return BookingClient(BOOKER_BASE_URL)

@pytest.fixture(scope="session")
def auth_token(client: BookingClient):
    response = client.auth(BOOKER_USERNAME, BOOKER_PASSWORD)
    assert response.status_code == 200
    token = response.json().get("token")
    assert token, f"Auth failed: {response.text}"
    return token

@pytest.fixture
def booking(client: BookingClient, auth_token: str):
    booking_data =  valid_booking()
    response = client.create_booking(booking_data)
    assert response.status_code == 200, response.text
    booking_id = response.json().get("bookingid")
    assert booking_id, f"Booking creation failed: {response.text}"
    yield {"id": booking_id, "data": booking_data}
    client.delete_booking(booking_id, auth_token)
