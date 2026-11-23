import pytest

pytestmark = pytest.mark.smoke


def test_get_bookings_returns_list(client):
    response = client.get_bookings()
    assert response.status_code == 200
    assert isinstance(response.json(), list)