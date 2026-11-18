import requests

class BookingClient:
    def __init__(self, base_url: str):
        """Initializes the booking client with the base URL of the API."""
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json",
                                    "Accept" : "application/json"})

    def get_bookings(self) -> requests.Response:
        """Retrieves all bookings from the API."""
        return self.session.get(self.base_url + "/booking")

    def auth(self, username: str, password: str) -> requests.Response:
        """Authenticates with the API and returns the response."""
        return self.session.post(self.base_url + "/auth", json={"username": username, "password": password})

    def create_booking(self, booking_data: dict) -> requests.Response:
        """Creates a new booking in the API."""
        return self.session.post(self.base_url + "/booking", json=booking_data)

    def get_booking(self, booking_id: int) -> requests.Response:
        """Retrieves a booking from the API."""
        return self.session.get(f"{self.base_url}/booking/{booking_id}")

    def update_booking(self, booking_id: int, booking_data: dict, token: str | None=None) -> requests.Response:
        """Updates a booking in the API."""
        
        headers = {"Cookie": f"token={token}"} if token else {}
        return self.session.put(f"{self.base_url}/booking/{booking_id}", json=booking_data, headers=headers)

    def delete_booking(self, booking_id: int, token: str | None=None) -> requests.Response:
        """Deletes a booking from the API."""
        headers = {"Cookie": f"token={token}"} if token else {}
        return self.session.delete(f"{self.base_url}/booking/{booking_id}", headers=headers)
