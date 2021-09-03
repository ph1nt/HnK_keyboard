"""Animate underglow LEDs
Metrhod:
    go() make animation step
Returns:
    Should never ends"""
import time

# pylint: disable=import-error
import board
import neopixel

# pylint: enable=import-error


class RGB:
    """RGB underglow with neopixels"""

    pin = board.GP28
    time = int(time.monotonic() * 10)
    intervals = (30, 20, 10, 5)
    reverse_animation = False
    effect_init = False
    enabled = True
    disable_auto_write = False

    def __init__(self, leds=12, pin=board.GP28):
        self.hue = 0
        self.sat = 255
        self.val = 25
        self.num_pixels = leds
        self.pin = pin
        self.hue_step = 5
        self.sat_step = 5
        self.val_step = 5
        self.hue = 0
        self.sat = 100
        self.val = 40
        self.val_limit = 150
        self.breathe_center = "breathe_center"
        self.knight_effect_length = "knight_effect_length"
        self.animation_mode = "user"
        self.animation_speed = 0.2
        self.user_animation = "user"
        self.intervals = (30, 20, 10, 5)
        self.neopixel = neopixel.NeoPixel(
            self.pin, self.num_pixels, brightness=self.val, auto_write=True
        )
        self.go()

    def __call__(self, *args, **kwds):
        self.go()

    def time_ms(self):
        return int(time.monotonic() * 1000)

    def hsv_to_rgb(self, hue, sat, val):
        """Converts HSV values, and returns a tuple of RGB values :return: (r, g, b)"""
        if val > self.val_limit:
            val = self.val_limit
        if sat == 0:
            r = val
            g = val
            b = val
        else:
            base = ((100 - sat) * val) / 100
            color = int((val - base) * ((hue % 60) / 60))
            x = int(hue / 60)
            if x == 0:
                r = val
                g = base + color
                b = base
            elif x == 1:
                r = val - color
                g = val
                b = base
            elif x == 2:
                r = base
                g = val
                b = base + color
            elif x == 3:
                r = base
                g = val - color
                b = val
            elif x == 4:
                r = base + color
                g = base
                b = val
            elif x == 5:
                r = val
                g = base
                b = val - color
        return int(r), int(g), int(b)

    def set_hsv(self, hue, sat, val, index):
        """Takes HSV values and displays it on a single LED/Neopixel"""
        self.set_rgb(self.hsv_to_rgb(hue, sat, val), index)
        return self

    def set_hsv_fill(self, hue, sat, val):
        """Takes HSV values and displays it on all LEDs/Neopixels"""
        self.set_rgb_fill(self.hsv_to_rgb(hue, sat, val))
        return self

    def set_rgb(self, rgb, index):
        """Takes an RGB and displays it on a single LED/Neopixel"""
        if 0 <= index <= self.num_pixels - 1:
            self.neopixel[index] = rgb
            if not self.disable_auto_write:
                self.neopixel.show()
        return self

    def set_rgb_fill(self, rgb):
        """Takes an RGB or RGBW and displays it on all LEDs/Neopixels:param rgb: RGB or RGBW"""
        if self.neopixel:
            self.neopixel.fill(rgb)
            if not self.disable_auto_write:
                self.neopixel.show()
        return self

    def off(self):
        """Turns off all LEDs/Neopixels without changing stored values"""
        self.set_hsv_fill(0, 0, 0)
        return self

    def show(self):
        """Turns on all LEDs/Neopixels without changing stored values"""
        self.neopixel.show()
        return self

    def go(self):
        """Activates a "step" in the animation. Returns the new state in animation"""
        if self._animation_step():
            return self.light_show()
        return self

    def _animation_step(self):
        if self.time_ms() - self.time >= 30:
            self.time = self.time_ms()
            return max(self.intervals)
        return False

    def _check_update(self):
        if self.animation_mode == "static_standby":
            return True

    def _do_update(self):
        if self.animation_mode == "static_standby":
            self.animation_mode = "static"

    def effect_static(self):
        self.set_hsv_fill(self.hue, self.sat, self.val)
        self.animation_mode = "static_standby"
        return self

    def light_show(self):
        """This is the code that is run every cycle that can serve as an animation"""
        self.hue = (self.hue + self.animation_speed) % 360
        self.disable_auto_write = True  # Turn off instantly showing
        for i in range(0, self.num_pixels):
            self.set_hsv(
                (self.hue - (i * self.num_pixels)) % 360, self.sat, self.val, i
            )
        # Show final results
        self.disable_auto_write = False  # Resume showing changes
        self.show()
        return self
