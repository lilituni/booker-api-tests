
import time
import functools


def retry(times: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """Decorator to retry a function call if it raises an exception."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times - 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"Retrying {func.__name__} due to error: {e}")
                    time.sleep(delay)
            return func(*args, **kwargs)  # Final attempt without catching exceptions
        return wrapper
    return decorator


