
import pytest

from utils.retry import retry

def test_retry_succeeds_after_failures():
    calls = {"count": 0}

    @retry(times=3, delay=0)
    def flaky():
        calls["count"] += 1
        if calls["count"] < 3:
            raise ConnectionError("service down")
        return "ok"

    assert flaky() == "ok"
    assert calls["count"] == 3


def test_retry_raises_after_last_attempt():
    calls = {"count": 0}

    @retry(times=2, delay=0, exceptions=(ConnectionError,))
    def always_fails():
        calls["count"] += 1
        raise ConnectionError("service down")

    with pytest.raises(ConnectionError):
        always_fails()
    assert calls["count"] == 2 


def test_retry_does_not_retry_other_exceptions():
    calls = {"count": 0}

    @retry(times=3, delay=0, exceptions=(ConnectionError,))
    def buggy():
        calls["count"] += 1
        raise KeyError("real bug")

    with pytest.raises(KeyError):
        buggy()
    assert calls["count"] == 1      # failed immediately, no retries