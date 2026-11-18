import requests

BASE_URL = "https://restful-booker.herokuapp.com"

def test_get_booking_returns_list():
    response = requests.get(BASE_URL + "/booking")
    assert response.status_code == 200
    assert isinstance(response.json(), list)