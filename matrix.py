"""Keyboard matrix"""

import time

# pylint: disable=import-error
import digitalio

# pylint: enable=import-error


class Matrix:
    """Implement the drive of keyboard matrix and provide an event queue"""

    def __init__(self, row_pins, col_pins, diode):
        self.keys = len(row_pins) * len(col_pins)
        self.queue = []  # bytearray(self.keys)
        for _n in range(self.keys):
            self.queue.append(0x000000)
        self.head = 0
        self.tail = 0
        self.length = 0
        self.rows = []  # row as output
        for pin in row_pins:
            inout = digitalio.DigitalInOut(pin)
            inout.direction = digitalio.Direction.OUTPUT
            inout.drive_mode = digitalio.DriveMode.PUSH_PULL
            inout.value = 0
            self.rows.append(inout)
        self.cols = []  # col as input
        for pin in col_pins:
            inout = digitalio.DigitalInOut(pin)
            inout.direction = digitalio.Direction.INPUT
            inout.pull = digitalio.Pull.DOWN if diode else digitalio.Pull.UP
            self.cols.append(inout)
        # row selected value depends on diodes' direction
        self.pressed = bool(diode)
        self.t0 = [0] * self.keys  # key pressed time
        self.t1 = [0] * self.keys  # key released time
        self.mask = 0
        self._debounce_time = 20_000_000  # nano seconds

    def scan(self):
        """
        Scan keyboard matrix and save key event into the queue.
        :return: length of the key event queue.
        """
        t = time.monotonic_ns()
        # use local variables to speed up
        pressed = self.pressed
        last_mask = self.mask
        cols = self.cols
        mask = 0
        key_index = -1
        for row in self.rows:
            row.value = pressed  # select row
            for col in cols:
                key_index += 1
                if col.value == pressed:
                    key_mask = 1 << key_index
                    if not last_mask & key_mask:
                        if t - self.t1[key_index] < self._debounce_time:
                            print("debonce")
                            continue
                        self.t0[key_index] = t
                        self.put(key_index)
                    mask |= key_mask
                elif last_mask and (last_mask & (1 << key_index)):
                    if t - self.t0[key_index] < self._debounce_time:
                        print("debonce")
                        mask |= 1 << key_index
                        continue
                    self.t1[key_index] = t
                    self.put(0x800000 | key_index)
            row.value = not pressed
        self.mask = mask
        return self.length

    def wait(self, timeout=1000):
        """Wait for a new key event or timeout"""
        last = self.length
        if timeout:
            end_time = time.monotonic_ns() + timeout * 1000000
            while True:
                _n = self.scan()
                if _n > last or time.monotonic_ns() > end_time:
                    return _n
        else:
            while True:
                _n = self.scan()
                if _n > last:
                    return _n

    def put(self, data):
        """Put a key event into the queue"""
        self.queue[self.head] = data
        self.head += 1
        if self.head >= self.keys:
            self.head = 0
        self.length += 1

    def get(self):
        """Remove and return the first event from the queue."""
        data = self.queue[self.tail]
        self.tail += 1
        if self.tail >= self.keys:
            self.tail = 0
        self.length -= 1
        return data

    def view(self, _n):
        """Return the specified event"""
        return self.queue[(self.tail + _n) % self.keys]

    def __getitem__(self, _n):
        """Return the specified event"""
        return self.queue[(self.tail + _n) % self.keys]

    def __len__(self):
        """Return the number of events in the queue"""
        return self.length

    def get_keydown_time(self, key):
        """Return the key pressed time"""
        return self.t0[key]

    def get_keyup_time(self, key):
        """Return the key released time"""
        return self.t1[key]

    def time(self):
        """Return current time"""
        return time.monotonic_ns()

    def timems(self, t):
        """Convert time to milliseconds"""
        return t // 1000000

    @property
    def debounce_time(self):
        return self._debounce_time // 1000000

    @debounce_time.setter
    def debounce_time(self, t):
        """Set debounce time"""
        self._debounce_time = t * 1000000
