import requests

from config import BOOKER_BASE_URL

def test_get_booking_returns_list():
    response = requests.get(BOOKER_BASE_URL + "/booking")
    assert response.status_code == 200
    assert isinstance(response.json(), list)