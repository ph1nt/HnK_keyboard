"""define matrix of keys"""

from keys import KC, MT, MO, TT, SK

___ = KC.TRNS
xxx = KC.NO
RC = MT(KC.SLSH, KC.RCTRL)
SE = MT(KC.SPACE, KC.RSFT)
ES = MT(KC.ESC, KC.LSFT)
RG = MT(KC.BSPC, KC.RCMD)
RA = MT(KC.ENTER, KC.RALT)
LG = MT(KC.BSPC, KC.LCMD)
LA = MT(KC.ENTER, KC.LALT)
LC = MT(KC.Z, KC.LCTRL)
UNDS = SK(KC.MINUS, KC.LSFT)
Fn1 = MO(1)
Fn2 = MO(2)
NUM = TT(3)

# fmt: off
# ---------------------- Keymap ---------------------------------------------------------
keymap = [
    # layer 0
    [
        KC.N1,       KC.N2,       KC.N3,       KC.N4,       KC.N5,       ES,          Fn1,         KC.N6,       KC.N7,         KC.N8,         KC.N9,         KC.N0,           Fn2,         KC.LEFT,
        KC.Q,        KC.W,        KC.E,        KC.R,        KC.T,        NUM,         LA,          KC.Y,        KC.U,          KC.I,          KC.O,          KC.P,            RA,          KC.UP,
        KC.A,        KC.S,        KC.D,        KC.F,        KC.G,        KC.TAB,      KC.LCMD,     KC.H,        KC.J,          KC.K,          KC.L,          KC.SCLN,         RG,          KC.DOWN,         
        LC,          KC.X,        KC.C,        KC.V,        KC.B,        ___,         ___,         KC.N,        KC.M,          KC.COMMA,      KC.DOT,        KC.SLSH,         SE,          KC.RGHT,
    ],
    # layer 1 (left) Fn1
    [
        KC.F1,       KC.F2,       KC.F3,       KC.F4,       KC.F5,       ___,         Fn1,         KC.F6,       KC.F7,         KC.F8,         KC.F9,         KC.EJCT,         Fn2,         KC.HOME,
        KC.DEL,      KC.UP,       KC.BSPC,     ___,         ___,         ___,         ___,         KC.GRAVE,    UNDS,          KC.PLUS,       KC.MINUS,      KC.EQUAL,        ___,         KC.PGUP,
        KC.LEFT,     KC.DOWN,     KC.RGHT,     ___,         ___,         ___,         ___,         KC.LCBR,     KC.RCBR,       KC.LBRC,       KC.RBRC,       KC.QUOT,         ___,         KC.PGDN,
        ___,         ___,         ___,         ___,         ___,         ___,         ___,         KC.NUBS,     KC.TILDE,      ___,           KC.PIPE,       KC.BSLS,         ___,         KC.END,
    ],
    # layer 2 (right) Fn2
    [
        KC.F1,       KC.F2,       KC.F3,       KC.F4,       KC.F5,       ___,         Fn1,         KC.F6,       KC.F7,         KC.F8,         KC.F9,         KC.F10,          Fn2,         ___,
        KC.F11,      KC.F12,      KC.F13,      KC.F14,      KC.F15,      ___,         ___,         KC.F16,      ___,           KC.MRWD,       KC.MFFD,       KC.MPLY,         ___,         ___,
        KC.RGB_MK,   KC.RGB_MB,   KC.RGB_VAI,  KC.RGB_HUI,  KC.RGB_SAI,  ___,         ___,         KC.RGB_TOG,  KC.RGB_MP,     KC.VOLD,       KC.VOLU,       KC.MUTE,         ___,         ___,
        KC.RGB_MR,   KC.RGB_MBR,  KC.RGB_VAD,  KC.RGB_HUD,  KC.RGB_SAD,  ___,         ___,         KC.RGB_LS,   ___,           ___,           ___,           ___,             KC.CAPS,     ___,
    ],
    # layer 3 (NUM)
    [
        ___,         ___,         ___,         ___,         ___,         ES,          ___,         ___,         KC.N7,         KC.N8,         KC.N9,         KC.PSLS,         ___,         ___,
        KC.PWR,      ___,         ___,         ___,         ___,         NUM,         ___,         ___,         KC.N4,         KC.N5,         KC.N6,         KC.PAST,         ___,         ___,
        ___,         ___,         ___,         ___,         ___,         ___,         ___,         ___,         KC.N1,         KC.N2,         KC.N3,         KC.PMNS,         ___,         ___,
        ___,         ___,         ___,         ___,         ___,         ___,         ___,         ___,         KC.N0,         KC.COMMA,      KC.DOT,        KC.PPLS,         KC.PEQL,     ___,
    ],
]
# fmt: on
