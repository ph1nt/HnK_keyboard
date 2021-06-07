import time
import math


def sleep_ms(ms):
    ''' sleep for a number of milliseconds '''
    return time.sleep(ms / 1000)


def ticks_ms():
    return math.floor(time.monotonic() * 1000)


def ticks_diff(new, old):
    return new - old
