def test_get_bookings_returns_list(client):
    response = client.get_bookings()
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_booking_returns_created_data(client, booking):
    response = client.get_booking(booking["id"])
    assert response.status_code == 200
    data = response.json()
    assert data == booking["data"], f"Expected {booking['data']}, got {data}"