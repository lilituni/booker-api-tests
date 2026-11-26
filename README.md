# booker-api-tests

[![tests](https://github.com/lilituni/booker-api-tests/actions/workflows/tests.yml/badge.svg)](https://github.com/lilituni/booker-api-tests/actions/workflows/tests.yml)

An API test automation framework in **Python and pytest** for [Restful Booker](https://restful-booker.herokuapp.com), a public practice API for hotel bookings.

It shows how I set up a maintainable test framework from scratch: a reusable API client, fixtures with guaranteed cleanup, risk-based coverage, and CI on every push.

## What's covered

| Area | What is checked | Where |
|---|---|---|
| **Smoke** | The API is up, a booking can be created, and it reads back correctly | marker `smoke` |
| **Create** | Returns a positive booking ID and the data that was sent | `tests/test_booking_crud.py` |
| **Read** | A created booking reads back unchanged; an unknown ID returns 404 | `tests/test_booking_crud.py` |
| **Update** | With a valid token, the response **and the saved data** change. Without a token or with an invalid one: 403, and the saved data stays unchanged | `tests/test_booking_crud.py` |
| **Delete** | With a valid token, the booking is gone (404). Without a token or with an invalid one: 403, and the booking still exists | `tests/test_booking_crud.py` |
| **Framework** | Unit tests for the retry decorator: retries until success, raises after the last attempt, doesn't retry unexpected errors | `tests/test_retry.py` |

## Design

```
clients/booking_client.py   How to call the API (tests never call requests directly)
data/bookings.py            Test data builder and the Booking class
conftest.py                 Fixtures: setup and cleanup
tests/                      What to check
utils/retry.py              Retry decorator (unit-tested, not applied to API calls yet)
```

- **One API client.** If the API changes, it is fixed in one place, not in every test.
- **Factory fixture for cleanup.** Every booking a test creates goes through `create_booking`, which records its ID and deletes it after the test, even if the test fails. `booking` gives tests a ready-made booking through the same factory.
- **Session-scoped client and token.** Created once per run, which keeps the suite fast. Bookings are function-scoped, so tests never share data.
- **Unique test data.** `valid_booking(**overrides)` builds valid data with a unique name; tests override only the fields they care about.
- **Stored state, not just responses.** After update and delete calls, tests read the booking back to check what was actually saved.
- **Own data only.** The API is public and resets regularly, so tests create the data they need and never rely on existing records.
- **No secrets in the repo.** Credentials come from environment variables or a local `.env` file, which is git-ignored.

## How to run

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows
# source .venv/bin/activate       # macOS / Linux

pip install -r requirements.txt
copy .env.example .env            # Windows (cp on macOS / Linux)
```

Set `BOOKER_PASSWORD` in `.env` to the demo password from the Restful Booker documentation. Then:

```bash
pytest -v            # full suite
pytest -m smoke      # smoke tests only
```

## CI

GitHub Actions runs the full suite on every push and pull request (`.github/workflows/tests.yml`). The password is stored as the repository secret `BOOKER_PASSWORD`, and a JUnit XML report is uploaded as a build artifact.

## Bugs found

| # | Request | Expected | Actual | Impact |
|---|---|---|---|---|
| 1 | `POST /auth` with a wrong password | 401 Unauthorized | 200 OK with `{"reason": "Bad credentials"}` | A client that checks only the status code treats a failed login as a success |

Bug 1 was caught because the `auth_token` fixture checks that a token is actually returned, not only the status code.

### Observations

Not bugs, but different from common REST conventions:

| Request | Convention | Actual |
|---|---|---|
| `DELETE /booking/{id}` | 200 OK or 204 No Content | 201 Created |
| `POST /booking` | 201 Created | 200 OK |

## Out of scope

Restful Booker is a shared public practice API, so some important kinds of testing are not possible or not responsible here:

| Area | Why it's out of scope here | How I'd cover it on a real project |
|---|---|---|
| **Database checks** | There is no access to the API's database | Query the database after each write, e.g. `SELECT` the booking by ID and compare it with the request. Here, a follow-up `GET` checks the stored state instead. |
| **Rate limiting** | No limits are documented, and flooding a shared public API would affect other users | Send requests above the documented limit and expect `429 Too Many Requests` with a `Retry-After` header |
| **Load and performance** | It runs on shared free hosting, so results wouldn't be meaningful, and the load would affect other users | Load tests with a tool such as JMeter or k6 against a dedicated environment |
| **Concurrency** | There is no documented behavior for two simultaneous updates (no ETags or version numbers), so there is nothing to assert | Two parallel updates to one record; expect the agreed behavior, e.g. `409 Conflict` or `412 Precondition Failed` |
| **Pagination** | The API has no pagination: `GET /booking` returns all IDs in one list | Check page size, the last page, an empty page, invalid page parameters, and that no record is repeated or skipped between pages |

## Roadmap

- [ ] Auth tests: valid login, wrong password, missing or invalid token on protected endpoints
- [ ] Parametrized validation tests for invalid booking data
- [ ] `Content-Type` header checks
- [ ] Response schema validation with pydantic
- [ ] Idempotency: deleting the same booking twice
- [ ] Filtering with query parameters
- [ ] Invalid payload handling (malformed JSON, wrong content type)
- [ ] Response time checks
