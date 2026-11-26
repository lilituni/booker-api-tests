import pytest
from data.bookings import valid_booking

@pytest.mark.smoke
def test_create_booking_returns_id_and_sent_data(create_booking):
    data = valid_booking()
    response = create_booking(data)
    assert response.status_code == 200
    body  = response.json()
    assert isinstance(body["bookingid"], int) and body["bookingid"] > 0
    assert body.get("booking") == data, f"Expected booking data {data}, got {body.get('booking')}"


@pytest.mark.smoke
def test_get_booking_returns_created_data(client, booking):
    response = client.get_booking(booking.id)
    assert response.status_code == 200
    data = response.json()
    assert data == booking.data, f"Expected {booking.data}, got {data}"


def test_get_unknown_booking_returns_404(client):
    response = client.get_booking(999999)  # Assuming this ID does not exist
    assert response.status_code == 404, f"Expected status code 404, got {response.status_code}"


def test_update_booking_with_token_changes_data(client, booking, auth_token):
    booking_data = valid_booking(firstname="UpdatedName")
    response = client.update_booking(booking.id, booking_data, auth_token)
    assert response.status_code == 200
    data = response.json()
    assert data == booking_data, f"Expected {booking_data}, got {data}"
    saved = client.get_booking(booking.id).json()
    assert saved == booking_data, f"Expected saved {booking_data}, got {saved}"


def test_update_booking_without_token_is_denied(client, booking):
    booking_data = valid_booking(firstname="UpdatedName")
    response = client.update_booking(booking.id, booking_data)
    assert response.status_code == 403, f"Expected status code 403, got {response.status_code}"
    saved = client.get_booking(booking.id).json()
    assert saved == booking.data, f"Expected saved {booking.data}, got {saved}"


def test_update_booking_with_invalid_token_is_denied(client, booking):
    booking_data = valid_booking(firstname="UpdatedName")
    response = client.update_booking(booking.id, booking_data, token="invalid_token")
    assert response.status_code == 403, f"Expected status code 403, got {response.status_code}"
    saved = client.get_booking(booking.id).json()
    assert saved == booking.data, f"Expected saved {booking.data}, got {saved}"

    
def test_delete_booking_removes_booking(client, booking, auth_token):
    response = client.delete_booking(booking.id, auth_token)
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
    # Verify that the booking is deleted
    get_response = client.get_booking(booking.id)
    assert get_response.status_code == 404, f"Expected status code 404 for deleted booking, got {get_response.status_code}"


def test_delete_booking_without_token_is_denied(client, booking):
    response = client.delete_booking(booking.id)
    assert response.status_code == 403, f"Expected status code 403, got {response.status_code}"
    get_response = client.get_booking(booking.id)
    assert get_response.status_code == 200, "Booking was deleted without valid authorization!"


def test_delete_booking_with_invalid_token_is_denied(client, booking):
    response = client.delete_booking(booking.id, token="invalid_token")
    assert response.status_code == 403, f"Expected status code 403, got {response.status_code}"
    get_response = client.get_booking(booking.id)
    assert get_response.status_code == 200, "Booking was deleted without valid authorization!"