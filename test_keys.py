keys = {}

KEY_SIMPLE = 0
KEY_MODIFIER = 1
KEY_CONSUMER = 2
KEY_MOUSE = 3
KEY_LAYER = 4
KEY_MODTAP = 5


def test(desc=""):
    for k in keys:
        n, t, m = keys[k]
        print("{}: {},".format(k, n))
    keys.clear()
    print("# {}".format(desc))


class AttrDict(dict):
    def __getattr__(self, _key):
        """Support for accessing dictionary entries in dot notation like `k.KC_ESC` rather than `k['KC_ESC']`"""
        return self[_key]


class key:
    def __init__(self, code=0, names=tuple(), key_type=0, key_next=None):
        self.code = code
        self.type = key_type
        self.names = names
        self.next = key_next


KC = AttrDict()
print(KC)
for n in KC:
    print(n)


def MT(key1=None, key2=None):
    return key1 + key2


def MO(layer=None):
    return layer


def TT(layer=None):
    return layer


def make_key(code=0, names=tuple(), key_type=0, next_key=None):
    """Create a new key, aliased by `names` in the KC lookup table."""
    if not key_type:
        keys[code] = (names, "KC.TYPE", next_key)
    elif key_type == KEY_CONSUMER:
        keys[code] = (names, "KC.CC", next_key)
    elif key_type == KEY_MODIFIER:
        keys[code] = (names, "KC.MOD", next_key)
    elif key_type == KEY_LAYER:
        keys[code] = (names, "KC.LL", next_key)
    for name in names:
        KC[name] = code


def make_shifted_key(target_name, names=tuple()):
    for i in keys:
        _names, _type, _next = keys[i]
        if target_name in _names:
            make_key(i, names)
    return key


test("Null keys")
make_key(0, ("TRNS",))
make_key(1, ("NO",))

test("Modifiers")
make_key(code=224, names=("LEFT_CONTROL", "LCTRL", "LCTL"), key_type=KEY_MODIFIER)
make_key(code=225, names=("LEFT_SHIFT", "LSHIFT", "LSFT"), key_type=KEY_MODIFIER)
make_key(code=226, names=("LEFT_ALT", "LALT"), key_type=KEY_MODIFIER)
make_key(code=227, names=("LEFT_SUPER", "LGUI", "LCMD", "LWIN"), key_type=KEY_MODIFIER)
make_key(code=228, names=("RIGHT_CONTROL", "RCTRL", "RCTL"), key_type=KEY_MODIFIER)
make_key(code=229, names=("RIGHT_SHIFT", "RSHIFT", "RSFT"), key_type=KEY_MODIFIER)
make_key(code=230, names=("RIGHT_ALT", "RALT"), key_type=KEY_MODIFIER)
make_key(code=231, names=("RIGHT_SUPER", "RGUI", "RCMD", "RWIN"), key_type=KEY_MODIFIER)

test("Basic ASCII letters")
make_key(code=4, names=("A",))
make_key(code=5, names=("B",))
make_key(code=6, names=("C",))
make_key(code=7, names=("D",))
make_key(code=8, names=("E",))
make_key(code=9, names=("F",))
make_key(code=10, names=("G",))
make_key(code=11, names=("H",))
make_key(code=12, names=("I",))
make_key(code=13, names=("J",))
make_key(code=14, names=("K",))
make_key(code=15, names=("L",))
make_key(code=16, names=("M",))
make_key(code=17, names=("N",))
make_key(code=18, names=("O",))
make_key(code=19, names=("P",))
make_key(code=20, names=("Q",))
make_key(code=21, names=("R",))
make_key(code=22, names=("S",))
make_key(code=23, names=("T",))
make_key(code=24, names=("U",))
make_key(code=25, names=("V",))
make_key(code=26, names=("W",))
make_key(code=27, names=("X",))
make_key(code=28, names=("Y",))
make_key(code=29, names=("Z",))

test("Numbers")
make_key(code=30, names=("1", "N1"))
make_key(code=31, names=("2", "N2"))
make_key(code=32, names=("3", "N3"))
make_key(code=33, names=("4", "N4"))
make_key(code=34, names=("5", "N5"))
make_key(code=35, names=("6", "N6"))
make_key(code=36, names=("7", "N7"))
make_key(code=37, names=("8", "N8"))
make_key(code=38, names=("9", "N9"))
make_key(code=39, names=("0", "N0"))

test("More ASCII standard keys")
make_key(code=40, names=("ENTER", "ENT", "\n"))
make_key(code=41, names=("ESCAPE", "ESC"))
make_key(code=42, names=("BACKSPACE", "BSPC"))
make_key(code=43, names=("TAB", "\t"))
make_key(code=44, names=("SPACE", " "))
make_key(code=45, names=("MINUS", "-"))
make_key(code=46, names=("EQUAL", "="))
make_key(code=47, names=("LBRACKET", "LBRC", "["))
make_key(code=48, names=("RBRACKET", "RBRC", "]"))
make_key(code=49, names=("BACKSLASH", "BSLS", "\\"))
make_key(code=51, names=("SEMICOLON", "SCLN", ";"))
make_key(code=52, names=("QUOTE", "QUOT", "'"))
make_key(code=53, names=("GRAVE", "`"))
make_key(code=54, names=("COMMA", ","))
make_key(code=55, names=("DOT", "."))
make_key(code=56, names=("SLASH", "SLSH"))

test("Function Keys")
make_key(code=58, names=("F1",))
make_key(code=59, names=("F2",))
make_key(code=60, names=("F3",))
make_key(code=61, names=("F4",))
make_key(code=62, names=("F5",))
make_key(code=63, names=("F6",))
make_key(code=64, names=("F7",))
make_key(code=65, names=("F8",))
make_key(code=66, names=("F9",))
make_key(code=67, names=("F10",))
make_key(code=68, names=("F11",))
make_key(code=69, names=("F12",))
make_key(code=104, names=("F13",))
make_key(code=105, names=("F14",))
make_key(code=106, names=("F15",))
make_key(code=107, names=("F16",))
make_key(code=108, names=("F17",))
make_key(code=109, names=("F18",))
make_key(code=110, names=("F19",))
make_key(code=111, names=("F20",))
make_key(code=112, names=("F21",))
make_key(code=113, names=("F22",))
make_key(code=114, names=("F23",))
make_key(code=115, names=("F24",))

test("Lock Keys, Navigation, etc.")
make_key(code=57, names=("CAPS_LOCK", "CAPSLOCK", "CAPS"))
make_key(code=70, names=("PRINT_SCREEN", "PSCREEN", "PSCR"))
make_key(code=71, names=("SCROLL_LOCK", "SCROLLLOCK", "SLCK"))
make_key(code=72, names=("PAUSE", "PAUS", "BRK"))
make_key(code=73, names=("INSERT", "INS"))
make_key(code=74, names=("HOME",))
make_key(code=75, names=("PGUP",))
make_key(code=76, names=("DELETE", "DEL"))
make_key(code=77, names=("END",))
make_key(code=78, names=("PGDOWN", "PGDN"))
make_key(code=79, names=("RIGHT", "RGHT"))
make_key(code=80, names=("LEFT",))
make_key(code=81, names=("DOWN",))
make_key(code=82, names=("UP",))

test("Numpad")
make_key(code=83, names=("NUM_LOCK", "NUMLOCK", "NLCK"))
make_key(code=84, names=("KP_SLASH", "NUMPAD_SLASH", "PSLS"))
make_key(code=85, names=("KP_ASTERISK", "NUMPAD_ASTERISK", "PAST"))
make_key(code=86, names=("KP_MINUS", "NUMPAD_MINUS", "PMNS"))
make_key(code=87, names=("KP_PLUS", "NUMPAD_PLUS", "PPLS"))
make_key(code=88, names=("KP_ENTER", "NUMPAD_ENTER", "PENT"))
make_key(code=89, names=("KP_1", "P1", "NUMPAD_1"))
make_key(code=90, names=("KP_2", "P2", "NUMPAD_2"))
make_key(code=91, names=("KP_3", "P3", "NUMPAD_3"))
make_key(code=92, names=("KP_4", "P4", "NUMPAD_4"))
make_key(code=93, names=("KP_5", "P5", "NUMPAD_5"))
make_key(code=94, names=("KP_6", "P6", "NUMPAD_6"))
make_key(code=95, names=("KP_7", "P7", "NUMPAD_7"))
make_key(code=96, names=("KP_8", "P8", "NUMPAD_8"))
make_key(code=97, names=("KP_9", "P9", "NUMPAD_9"))
make_key(code=98, names=("KP_0", "P0", "NUMPAD_0"))
make_key(code=99, names=("KP_DOT", "PDOT", "NUMPAD_DOT"))
make_key(code=103, names=("KP_EQUAL", "PEQL", "NUMPAD_EQUAL"))
make_key(code=133, names=("KP_COMMA", "PCMM", "NUMPAD_COMMA"))
make_key(code=134, names=("KP_EQUAL_AS400", "NUMPAD_EQUAL_AS400"))

test("Shift + whatever key")
make_shifted_key("GRAVE", names=("TILDE", "TILD", "~"))
make_shifted_key("1", names=("EXCLAIM", "EXLM", "!"))
make_shifted_key("2", names=("AT", "@"))
make_shifted_key("3", names=("HASH", "POUND", "#"))
make_shifted_key("4", names=("DOLLAR", "DLR", "$"))
make_shifted_key("5", names=("PERCENT", "PERC", "%"))
make_shifted_key("6", names=("CIRCUMFLEX", "CIRC", "^"))
make_shifted_key("7", names=("AMPERSAND", "AMPR", "&"))
make_shifted_key("8", names=("ASTERISK", "ASTR", "*"))
make_shifted_key("9", names=("LEFT_PAREN", "LPRN", "("))
make_shifted_key("0", names=("RIGHT_PAREN", "RPRN", ")"))
make_shifted_key("MINUS", names=("UNDERSCORE", "UNDS", "_"))
make_shifted_key("EQUAL", names=("PLUS", "+"))
make_shifted_key("LBRACKET", names=("LEFT_CURLY_BRACE", "LCBR", "{"))
make_shifted_key("RBRACKET", names=("RIGHT_CURLY_BRACE", "RCBR", "}"))
make_shifted_key("BACKSLASH", names=("PIPE", "|"))
make_shifted_key("SEMICOLON", names=("COLON", "COLN", ":"))
make_shifted_key("QUOTE", names=("DOUBLE_QUOTE", "DQUO", "DQT", '"'))
make_shifted_key("COMMA", names=("LEFT_ANGLE_BRACKET", "LABK", "<"))
make_shifted_key("DOT", names=("RIGHT_ANGLE_BRACKET", "RABK", ">"))
make_shifted_key("SLSH", names=("QUESTION", "QUES", "?"))

test("International")
make_key(code=50, names=("NONUS_HASH", "NUHS"))
make_key(code=100, names=("NONUS_BSLASH", "NUBS"))
make_key(code=101, names=("APP", "APPLICATION", "SEL", "WINMENU"))
make_key(code=102, names=("PWR",))
make_key(code=135, names=("INT1", "RO"))
make_key(code=136, names=("INT2", "KANA"))
make_key(code=137, names=("INT3", "JYEN"))
make_key(code=138, names=("INT4", "HENK"))
make_key(code=139, names=("INT5", "MHEN"))
make_key(code=140, names=("INT6",))
make_key(code=141, names=("INT7",))
make_key(code=142, names=("INT8",))
make_key(code=143, names=("INT9",))
make_key(code=144, names=("LANG1", "HAEN"))
make_key(code=145, names=("LANG2", "HAEJ"))
make_key(code=146, names=("LANG3",))
make_key(code=147, names=("LANG4",))
make_key(code=148, names=("LANG5",))
make_key(code=149, names=("LANG6",))
make_key(code=150, names=("LANG7",))
make_key(code=151, names=("LANG8",))
make_key(code=152, names=("LANG9",))
make_key(code=181, names=("ACCENT", "ACC"))

test("Consumer")
make_key(key_type=KEY_CONSUMER, code=226, names=("AUDIO_MUTE", "MUTE"))  # ('0xE2
make_key(key_type=KEY_CONSUMER, code=233, names=("AUDIO_VOL_UP", "VOLU"))  # ('0xE9
make_key(key_type=KEY_CONSUMER, code=234, names=("AUDIO_VOL_DOWN", "VOLD"))  # ('0xEA
make_key(key_type=KEY_CONSUMER, code=181, names=("MEDIA_NEXT_TRACK", "MNXT"))  # ('0xB5
make_key(key_type=KEY_CONSUMER, code=182, names=("MEDIA_PREV_TRACK", "MPRV"))  # ('0xB6
make_key(key_type=KEY_CONSUMER, code=183, names=("MEDIA_STOP", "MSTP"))  # ('0xB7
make_key(key_type=KEY_CONSUMER, code=205, names=("MEDIA_PLAY_PAUSE", "MPLY"))  # ('0xCD
make_key(key_type=KEY_CONSUMER, code=184, names=("MEDIA_EJECT", "EJCT"))  # ('0xB8
make_key(
    key_type=KEY_CONSUMER, code=179, names=("MEDIA_FAST_FORWARD", "MFFD")
)  # ('0xB3
make_key(key_type=KEY_CONSUMER, code=180, names=("MEDIA_REWIND", "MRWD"))  # ('0xB4

test("RGB")
make_key(1000, names=("RGB_TOG",))
make_key(1001, names=("RGB_HUI",))
make_key(1002, names=("RGB_HUD",))
make_key(1003, names=("RGB_SAI",))
make_key(1004, names=("RGB_SAD",))
make_key(1005, names=("RGB_VAI",))
make_key(1006, names=("RGB_VAD",))
make_key(1007, names=("RGB_ANI",))
make_key(1008, names=("RGB_AND",))
make_key(1009, names=("RGB_MODE_PLAIN", "RGB_MP"))
make_key(1010, names=("RGB_MODE_BREATHE", "RGB_MB"))
make_key(1011, names=("RGB_MODE_RAINBOW", "RGB_MR"))
make_key(1012, names=("RGB_MODE_BREATHE_RAINBOW", "RGB_MBR"))
make_key(1013, names=("RGB_MODE_SWIRL", "RGB_MS"))
make_key(1014, names=("RGB_MODE_KNIGHT", "RGB_MK"))
make_key(1015, names=("RGB_LIGHT_SHOW", "RGB_LS"))

test("Layers")
make_key(1016, key_type=KEY_LAYER, names=("MO",))
make_key(1017, key_type=KEY_LAYER, names=("DF",))
make_key(1018, key_type=KEY_LAYER, names=("LM",))
make_key(1019, key_type=KEY_LAYER, names=("LT",))
make_key(1020, key_type=KEY_LAYER, names=("TG",))
make_key(1021, key_type=KEY_LAYER, names=("TO",))
make_key(1022, key_type=KEY_LAYER, names=("TT",))
make_key(1023, key_type=KEY_MODTAP, names=("MT",))
test()

print(KC)
for n in KC:
    print(n)
