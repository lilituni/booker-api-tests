import pytest


@pytest.mark.smoke
def test_get_booking_returns_created_data(client, booking):
    response = client.get_booking(booking["id"])
    assert response.status_code == 200
    data = response.json()
    assert data == booking["data"], f"Expected {booking['data']}, got {data}"