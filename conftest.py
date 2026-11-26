import pytest
import requests
from config import BOOKER_BASE_URL, BOOKER_USERNAME, BOOKER_PASSWORD
from clients.booking_client import BookingClient
from data.bookings import Booking, valid_booking


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
def create_booking(client: BookingClient, auth_token: str):
    """Fixture to create a booking and ensure cleanup after the test.
    Yields a function that can be called to create a booking with given data."""
    created_ids = []

    def _create(data: dict) -> requests.Response:
        response = client.create_booking(data)
        if response.ok:
            booking_id = response.json().get("bookingid")
            if booking_id:
                created_ids.append(booking_id)
        return response
    yield _create
    for booking_id in created_ids:
        client.delete_booking(booking_id, auth_token)

@pytest.fixture
def booking(create_booking):
    """Fixture to create a booking and return its ID and data."""
    data = valid_booking()
    response = create_booking(data)
    assert response.status_code == 200
    booking_id = response.json().get("bookingid")
    assert booking_id, f"Booking creation failed: {response.text}"
    return Booking(id=booking_id, data=data)