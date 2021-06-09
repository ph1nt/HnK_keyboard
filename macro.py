# pylint: disable=import-error
import supervisor
# pylint: disable=import-error
from keyboard import layout


class macros:
    keyboard = object

    def __init__(self, _kbd) -> None:
        self.keyboard = _kbd
        self.keyboard.macro_handler = self.macro_handler
        self.keyboard.pairs_handler = self.pairs_handler

    def macro_handler(self, n, is_down):
        if is_down:
            if n == 1:
                layout.write('{')
            elif n == 2:
                layout.write('}')

    def pairs_handler(self, _n):
        layout.write('You just triggered pair keys #{}\n'.format(_n))
        if _n == 0:  # TAB + SPAPCE soft reboot
            print('SOFT REBOOT by key pairs: Tab + Shift')
            supervisor.reload()
        elif _n == 1:  # 1 + 6
            self.keyboard.layer_mask = 1
        else:
            print('wrong pairs index: {}'.format(_n))
