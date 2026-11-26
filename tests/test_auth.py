import pytest

from config import BOOKER_USERNAME, BOOKER_PASSWORD

@pytest.mark.smoke
def test_auth_with_valid_credentials_returns_token(client):
    response = client.auth(BOOKER_USERNAME, BOOKER_PASSWORD)
    assert response.status_code == 200
    token = response.json().get("token")
    assert token, "Token is empty in the response"
    assert isinstance(token, str), "Token is not a string"