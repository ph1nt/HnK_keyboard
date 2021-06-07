"""# HnK keyboard firmware

   https://github.com/ph1nt/HnK_keyboard.git

   single Raspberry Pi Pico (split keyboard)
   format style black, exept line lenght"""

# pylint: disable=import-error
import board
# pylint: enable=import-error
from log import debug
from rgb import RGB
from keyboard import kbdc

rgb = RGB(leds=12, pin=board.GP28)

row_pins = (board.GP5, board.GP4, board.GP3, board.GP2)
col_pins = (board.GP18, board.GP19, board.GP20, board.GP21, board.GP22, board.GP16, board.GP17,
            board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11, board.GP12)

debug.set(debug.INFO)

kbd = kbdc(row_pins, col_pins, True)

if __name__ == "__main__":
    debug.log(debug.INFO, "starting keyboard")
    while True:
        rgb()
        kbd()
