import array
import time
# pylint: disable=import-error
import board
import analogio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.mouse import Mouse
# pylint: enable=import-error
from matrix import Matrix
from key_map import keymap
from keys import KC

## from action_code
ACT_MODS = 0b0000
ACT_MODS_TAP = 0b0010
ACT_USAGE = 0b0100
ACT_MOUSEKEY = 0b0101
ACT_LAYER = 0b1000
ACT_LAYER_TAP = 0b1010    # Layer  0-15
ACT_LAYER_TAP_EXT = 0b1011    # Layer 16-31
ACT_MACRO = 0b1100
ACT_BACKLIGHT = 0b1101
ACT_COMMAND = 0b1110
ACT_FUNCTION = 0b1111
OP_BIT_AND = 0
OP_BIT_OR = 1
OP_BIT_XOR = 2
OP_BIT_SET = 3
ON_PRESS = 1
ON_RELEASE = 2
ON_BOTH = 3
OP_TAP_TOGGLE = 0xF0
MS_MOVEMENT = ((0, 0, 0), (0, -2, 0), (0, 2, 0),
               (-2, 0, 0), (2, 0, 0), (-1, -1, 0),
               (1, -1, 0), (-1, 1, 0), (1, 1, 0),
               (0, 0, 1), (0, 0, -1))


def mods_to_keycodes(mods):
    """ :return: list(filter(lambda k: mods & (1 << (k & 0x3)), all_mods)) """
    b = KC.RCTRL
    o = []
    for i in range(4):
        if (mods >> i + 4) & 1:
            o.append(b + i)
    b = KC.LCTRL
    for i in range(4):
        if (mods >> i) & 1:
            o.append(b + i)
    print('mods_to_keycodes {}'.format(o))
    return o


class analogMouse:
    def __init__(self, _km) -> None:
        self.km = _km
        self.x_axis = analogio.AnalogIn(board.A0)
        self.y_axis = analogio.AnalogIn(board.A1)
        self.x0 = 0
        for _n in range(5):
            self.x0 += self.get_voltage(self.x_axis)
        self.x0 = self.x0 / 5
        self.y0 = 0
        for _n in range(5):
            self.y0 += self.get_voltage(self.y_axis)
        self.y0 = self.y0 / 5
        self.deadZoneSize = 0.5
        pot_min = 0.00
        pot_max = 3.29
        self.step = (pot_max - pot_min) / 20.0

    def get_voltage(self, pin):
        return (pin.value * 3.3) / 65536

    def steps(self, axis, deadPoint):
        """ Maps the potentiometer voltage range to 0-20 """
        tmp = deadPoint - axis
        if abs(tmp) > self.deadZoneSize:
            return round(tmp / self.step)
        return 0

    def get(self):
        x = self.steps(self.get_voltage(self.x_axis), self.x0)
        y = self.steps(self.get_voltage(self.y_axis), self.y0)
        return(x, y)


kb = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kb)
kcc = ConsumerControl(usb_hid.devices)
km = Mouse(usb_hid.devices)
am = analogMouse(km)


def do_nothing(*_args, **_kargs):
    pass


class kbdc:
    def __init__(self, row_pins, col_pins, diode, _pairs):
        def convert(a):
            return array.array("L", (k for k in a))  # 4 bytes
        self.verbose = 1  # verbose
        self.pairs = _pairs
        self.pairs_handler = do_nothing
        self.pair_keys = set()
        for pair in self.pairs:
            for key in pair:
                print('pair key:{}'.format(key))
                self.pair_keys.add(key)
        print(self.pair_keys)
        self.macro_handler = do_nothing
        self.layer_mask = 1
        self.matrix = Matrix(row_pins, col_pins, diode)
        self.tap_delay = 500
        self.fast_type_thresh = 200
        self.pair_delay = 50
        self.adv_timeout = None
        self.actionmap = tuple(convert(layer) for layer in keymap)
        matrix = self.matrix
        self.keys = [0] * matrix.keys
        self.last_time = 0
        self.mouse_action = 0
        self.amouse_action = 0
        self.mouse_time = 0
        self.dt = 0
        self.dt2 = 0

    def get_key_sequence_info(self, start, end):
        """Get the info from a sequence of key events"""
        matrix = self.matrix
        event = matrix.view(start - 1)
        key = event & 0x7F
        desc = ""
        if event < 0x80:
            desc += " \\ "
            t0 = matrix.get_keydown_time(key)
        else:
            desc += " / "
            t0 = matrix.get_keyup_time(key)
        t = []
        for i in range(start, end):
            event = matrix.view(i)
            key = event & 0x7F
            if event < 0x80:
                desc += " \\ "
                t1 = matrix.get_keydown_time(key)
            else:
                desc += " / "
                t1 = matrix.get_keyup_time(key)
            dt = matrix.timems(t1 - t0)
            t0 = t1
            t.append(dt)
        return desc, t

    def is_tapping_key(self, key):
        """Check if the key is tapped (press & release quickly)"""
        matrix = self.matrix
        n = len(matrix)
        if n == 0:
            n = matrix.wait(self.tap_delay - matrix.timems(matrix.time() - matrix.get_keydown_time(key)))
        target = key | 0x800000
        if n >= 1:
            new_key = matrix.view(0)
            if new_key == target:
                return True
            if new_key >= 0x800000:
                # Fast Typing - B is a tap-key
                #   A↓      B↓      A↑      B↑
                # --+-------+-------+-------+------> t
                #           |  dt1  |
                #         dt1 < tap_delay
                if self.verbose:
                    desc, t = self.get_key_sequence_info(-1, n)
                    print(desc)
                    print(t)
                return True
            if n == 1:
                n = matrix.wait(self.fast_type_thresh - matrix.timems(matrix.time() - matrix.get_keydown_time(new_key)))
        if n < 2:
            return False
        if target == matrix.view(1):
            # Fast Typing - B is a tap-key
            #   B↓      C↓      B↑      C↑
            # --+-------+-------+-------+------> t
            #   |  dt1  |  dt2  |
            # dt1 < tap_delay && dt2 < fast_type_thresh
            if self.verbose:
                desc, t = self.get_key_sequence_info(-1, n)
                print(desc)
                print(t)
            return True
        if self.verbose:
            desc, t = self.get_key_sequence_info(-1, n)
            print(desc)
            print(t)
        return False

    def action_code(self, position):
        layer_mask = self.layer_mask
        for layer in range(len(self.actionmap) - 1, -1, -1):
            if (layer_mask >> layer) & 1:
                code = self.actionmap[layer][position]
                print('layer:{} code:{} position:{}'.format(layer, code, position))
                if code == 1:  # TRANSPARENT
                    continue
                return code
        return 0

    def log(self, *args):
        if self.verbose:
            print(*args)

    def send(self, *keycodes):
        self.press(*keycodes)
        self.release(*keycodes)

    def press(self, *keycodes):
        kb.press(*keycodes)

    def release(self, *keycodes):
        kb.release(*keycodes)

    def send_consumer(self, keycode):
        kcc.send(keycode)

    def press_mouse(self, buttons):
        km.press(buttons)

    def release_mouse(self, buttons):
        km.release(buttons)

    def move_mouse(self, x=0, y=0, wheel=0):
        km.move(x, y, wheel)

    def get(self):
        event = self.matrix.get()
        return event

    def __call__(self):
        t = 20 if (self.mouse_action or self.amouse_action) else 1000
        n = self.matrix.wait(t)
        if self.pair_keys:
            # detecting pair keys
            if n == 1:
                print('pair n == 1')
                key = self.matrix.view(0)
                if key < 0x800000 and key in self.pair_keys:
                    n = self.matrix.wait(self.pair_delay - self.matrix.timems(self.matrix.time() -
                                         self.matrix.get_keydown_time(key)))
            if n >= 2:
                print('pair n >= 2')
                pair = {self.matrix.view(0), self.matrix.view(1)}
                if pair in self.pairs:
                    pair_index = self.pairs.index(pair)
                    key1 = self.get()
                    key2 = self.get()
                    self.dt = self.matrix.timems(self.matrix.get_keydown_time(key2) -
                                                 self.matrix.get_keydown_time(key1))
                    self.pairs_handler(pair_index)
        while len(self.matrix):
            event = self.get()
            print('event:{} up:{}'.format(event & 0x7fffff, (event & 0x800000 != 0)))
            key = event & 0x7fffff
            if event & 0x800000 == 0:
                action_code = self.action_code(key)
                print('action_code:{:06x}'.format(action_code))
                self.keys[key] = action_code
                if action_code <= 0xFF:
                    self.press(action_code)
                else:
                    kind = action_code >> 16
                    print('kind:{:02x}'.format(kind))
                    if kind < ACT_MODS_TAP:
                        # MODS
                        mods = (action_code >> 8) & 0x1F
                        keycodes = mods_to_keycodes(mods)
                        print('ACT_MODS_TAP mods:{}, keycodes:{}'.format(mods, keycodes))  # DEBUG
                        keycodes.append(action_code & 0xFF)
                        self.press(*keycodes)
                    elif kind < ACT_USAGE:
                        # MODS_TAP
                        if self.is_tapping_key(key):
                            print('is_tapping_key')
                            keycode = action_code & 0xFF
                            self.keys[key] = keycode
                            self.press(keycode)
                        else:
                            mods = (action_code >> 8) & 0xFF
                            print('not_tapping_key mods:{:02x}'.format(mods))
                            keycodes = mods_to_keycodes(mods)
                            self.press(*keycodes)
                    elif kind == ACT_USAGE:
                        if action_code & 0x400:
                            self.send_consumer(action_code & 0x3FF)
                    elif kind == ACT_MOUSEKEY:
                        if action_code & 0xF00 == 0:
                            self.press_mouse(action_code & 0xF)
                        else:
                            mouse_action = (action_code >> 8) & 0xF
                            self.mouse_time = time.monotonic_ns()
                    elif kind == ACT_LAYER_TAP or kind == ACT_LAYER_TAP_EXT:
                        layer = (action_code >> 8) & 0x1F
                        mask = 1 << layer
                        if action_code & 0xE0 == 0xC0:
                            mods = action_code & 0x1F
                            keycodes = mods_to_keycodes(mods)
                            self.press(*keycodes)
                            self.layer_mask |= mask
                        elif self.is_tapping_key(key):
                            keycode = action_code & 0xFF
                            if keycode == OP_TAP_TOGGLE:
                                self.layer_mask = (self.layer_mask & ~mask) | (mask & ~self.layer_mask)
                                self.keys[key] = 0
                            else:
                                self.keys[key] = keycode
                                self.press(keycode)
                        else:
                            self.layer_mask |= mask
                    elif kind == ACT_MACRO:
                        if callable(self.macro_handler):
                            i = action_code & 0xFFF
                            self.macro_handler(i, True)
                if self.verbose:
                    keydown_time = self.matrix.get_keydown_time(key)
                    self.dt = 0
                    self.dt2 = 0
                    try:
                        self.dt = self.matrix.timems(self.matrix.time() - keydown_time)
                        self.dt2 = self.matrix.timems(keydown_time - self.last_time)
                    except OverflowError:
                        print("An exception flew by!")
                    finally:
                        self.last_time = keydown_time
            else:
                action_code = self.keys[key]
                if action_code < 0xFF:
                    self.release(action_code)
                else:
                    kind = action_code >> 12
                    if kind < ACT_MODS_TAP:
                        # MODS
                        mods = (action_code >> 8) & 0x1F
                        keycodes = mods_to_keycodes(mods)
                        keycodes.append(action_code & 0xFF)
                        self.release(*keycodes)
                    elif kind < ACT_USAGE:
                        # MODS_TAP
                        mods = (action_code >> 8) & 0x1F
                        keycodes = mods_to_keycodes(mods)
                        self.release(*keycodes)
                    elif kind == ACT_USAGE:
                        if action_code & 0x400:
                            self.send_consumer(0)
                    elif kind == ACT_MOUSEKEY:
                        if action_code & 0xF00 == 0:
                            self.release_mouse(action_code & 0xF)
                        elif (action_code >> 8) & 0xF == mouse_action:
                            mouse_action = 0
                            self.move_mouse(0, 0, 0)
                    elif kind == ACT_LAYER_TAP or kind == ACT_LAYER_TAP_EXT:
                        layer = (action_code >> 8) & 0x1F
                        keycode = action_code & 0xFF
                        if keycode & 0xE0 == 0xC0:
                            mods = keycode & 0x1F
                            keycodes = mods_to_keycodes(mods)
                            self.release(*keycodes)
                        self.layer_mask &= ~(1 << layer)
                    elif kind == ACT_MACRO:
                        i = action_code & 0xFFF
                        self.macro_handler(i, False)
                if self.verbose:
                    keyup_time = self.matrix.get_keyup_time(key)
                    self.dt = 0
                    self.dt2 = 0
                    try:
                        self.dt = self.matrix.timems(self.matrix.time() - keyup_time)
                        self.dt2 = self.matrix.timems(keyup_time - self.last_time)
                    except OverflowError:
                        print("An exception flew by!")
                    finally:
                        self.last_time = keyup_time
        if self.mouse_action:
            x, y, wheel = MS_MOVEMENT[mouse_action]
            self.dt = 1 + (time.monotonic_ns() - self.mouse_time) // 2000_000
            self.mouse_time = time.monotonic_ns()
            self.move_mouse(x * self.dt, y * self.dt, -1 * wheel)
        # analog mouse
        x, y = am.get()
        self.amouse_action = not((x == 0) & (y == 0))
        if self.layer_mask == 3:
            self.move_mouse(0, 0, x)
        else:
            self.move_mouse(x, y, 0)
