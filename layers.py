"""
DF(layer) - switches the default layer. The default layer is the always-active base layer that other layers stack on top of.
        See below for more about the default layer. This might be used to switch from QWERTY to Dvorak layout.
        Note that this is a temporary switch that only persists until the keyboard loses power.
MO(layer) - momentarily activates layer. As soon as you let go of the key, the layer is deactivated.
LM(layer, mod) - Momentarily activates layer (like MO), but with modifier(s) mod active. Only supports layers 0-15 and
        the left modifiers: MOD_LCTL, MOD_LSFT, MOD_LALT, MOD_LGUI (note the use of MOD_ constants instead of KC_).
        These modifiers can be combined using bitwise OR, e.g. LM(_RAISE, MOD_LCTL | MOD_LALT).
LT(layer, kc) - momentarily activates layer when held, and sends kc when tapped. Only supports layers 0-15.
OSL(layer) - momentarily activates layer until the next key is pressed.
        See One Shot Keys for details and additional functionality.
TG(layer) - toggles layer, activating it if it's inactive and vice versa.
TO(layer) - activates layer and de-activates all other layers (except your default layer).
        This function is special, because instead of just adding/removing one layer to your active layer stack,
        it will completely replace your current active layers, uniquely allowing you to replace higher layers with a lower one.
        This is activated on keydown (as soon as the key is pressed).
"""
from ktime import ticks_diff, ticks_ms


def df_pressed(key, state, *args, **kwargs):
    """Switches the default layer"""
    state.active_layers[-1] = key.meta.layer
    return state


def mo_pressed(key, state, *args, **kwargs):
    """Momentarily activates layer, switches off when you let go"""
    state.active_layers.insert(0, key.meta.layer)
    return state


def mo_released(key, state, KC, *args, **kwargs):
    """remove the first instance of the target layer from the active list
    under almost all normal use cases, this will disable the layer also resolves an issue where using DF()
    on a layer triggered by MO() and then defaulting to the MO()'s layer would result in no layers active"""
    try:
        del_idx = state.active_layers.index(key.meta.layer)
        del state.active_layers[del_idx]
    except ValueError:
        pass
    return state


def lm_pressed(key, state, *args, **kwargs):
    """As MO(layer) but with mod active"""
    state.hid_pending = True
    # Sets the timer start and acts like MO otherwise
    state.start_time["lm"] = ticks_ms()
    state.keys_pressed.add(key.meta.kc)
    return mo_pressed(key, state, *args, **kwargs)


def lm_released(key, state, *args, **kwargs):
    """As MO(layer) but with mod active"""
    state.hid_pending = True
    state.keys_pressed.discard(key.meta.kc)
    state.start_time["lm"] = None
    return mo_released(key, state, *args, **kwargs)


def lt_pressed(key, state, *args, **kwargs):
    # Sets the timer start and acts like MO otherwise
    state.start_time["lt"] = ticks_ms()
    return mo_pressed(key, state, *args, **kwargs)


def lt_released(key, state, *args, **kwargs):
    # On keyup, check timer, and press key if needed.
    if state.start_time["lt"] and (
        ticks_diff(ticks_ms(), state.start_time["lt"]) < state.config.tap_time
    ):
        state.hid_pending = True
        state.tap_key(key.meta.kc)

    mo_released(key, state, *args, **kwargs)
    state.start_time["lt"] = None
    return state


def tg_pressed(key, state, *args, **kwargs):
    """Toggles the layer (enables it if not active, and vise versa)"""
    # See mo_released for implementation details around this
    try:
        del_idx = state.active_layers.index(key.meta.layer)
        del state.active_layers[del_idx]
    except ValueError:
        state.active_layers.insert(0, key.meta.layer)
    return state


def to_pressed(key, state, *args, **kwargs):
    """Activates layer and deactivates all other layers"""
    state.active_layers.clear()
    state.active_layers.insert(0, key.meta.layer)
    return state


def tt_pressed(key, state, *args, **kwargs):
    """Momentarily activates layer if held, toggles it if tapped repeatedly"""
    # TODO Make this work with tap dance to function more correctly, but technically works.
    if state.start_time["tt"] is None:
        # Sets the timer start and acts like MO otherwise
        state.start_time["tt"] = ticks_ms()
        return mo_pressed(key, state, *args, **kwargs)
    elif ticks_diff(ticks_ms(), state.start_time["tt"]) < state.config.tap_time:
        state.start_time["tt"] = None
        return tg_pressed(key, state, *args, **kwargs)


def tt_released(key, state, *args, **kwargs):
    tap_timed_out = (
        ticks_diff(ticks_ms(), state.start_time["tt"]) >= state.config.tap_time
    )
    if state.start_time["tt"] is None or tap_timed_out:
        # On first press, works like MO. On second press, does nothing unless let up within
        # time window, then acts like TG.
        state.start_time["tt"] = None
        return mo_released(key, state, *args, **kwargs)
    return state
