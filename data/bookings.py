import uuid


def valid_booking(**overrides: object) -> dict:
    """Returns valid booking data. Override any field for a specific test."""
    data = {
        "firstname": f"Test-{uuid.uuid4().hex[:8]}",   # unique every time
        "lastname": "Tester",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-12-01", "checkout": "2026-12-05"},
        "additionalneeds": "Breakfast",
    }
    data.update(overrides)
    return data