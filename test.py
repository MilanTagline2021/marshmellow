import signal
from contextlib import contextmanager
import time
def long_function_call():
    time.sleep(2)
    print("hello world!!!")

class TimeoutException(Exception):
    pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


try:
    with time_limit(5):
        long_function_call()
except TimeoutException as e:
    print("Timed out!") 