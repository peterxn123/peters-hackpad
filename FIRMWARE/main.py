# hi there! really hope this would work, don't have anything to test it on lol

import board
import time
import asyncio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.scanners.encoder import RotaryioEncoder
from kmk.extensions.rgb import RGB
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler

keyboard = KMKKeyboard()

# keys:
keyboard.matrix = [
    KeysScanner(
        pins=[
            board.A0,  # GPIO26
            board.A1,  # GPIO27
            board.A2,  # GPIO28
            board.A3,  # GPIO29
            board.GP7, # GPIO0
            board.GP0  # GPIO1
        ],
        value_when_pressed=False,
        pull=True
    ),
    RotaryioEncoder(
        pin_a=board.GP2,
        pin_b=board.GP1
    )
]

keyboard.coord_mapping = [
    0, 1, 2, 3, 4, 5
]

# rgb:
rgb = RGB(
    pixel_pin=board.GP6,
    num_pixels=2,
    rgb_order=(1, 0, 2),  # GRB
    brightness_limit=255,
)
keyboard.extensions.append(rgb)

# encoder:
encoder_handler = EncoderHandler()
encoder_handler.encoder_map = [((KC.VOLD, KC.VOLU),)]
keyboard.modules.append(encoder_handler)

# keys:
keyboard.keymap = [
    [
        KC.LGUI(KC.D),      # show desktop
        KC.LGUI(KC.TAB),    # app switcher
        KC.LGUI(KC.L),      # lock screen
        KC.LGUI(KC.E),      # open windows explorer 
        KC.LCTL(KC.C),      # copy
        KC.LCTL(KC.V),      # paste
    ]
]

# blue when turned on
@keyboard.on_startup
def set_initial_leds():
    base_color = (0, 0, 50)
    rgb.set_rgb_value(0, base_color)
    rgb.set_rgb_value(1, base_color)

# super-duper cool animation on keypress
@keyboard.on_key
def animate_on_key(key, pressed, **kwargs):
    if pressed:
        pulse_animation()

def pulse_animation():
    # colour goes from blue to white gradually
    steps = 10
    for i in range(steps):
        val = int(255 * (i / steps))
        rgb.set_rgb_value(0, (val, val, val))
        rgb.set_rgb_value(1, (val, val, val))
        time.sleep(0.01)

    for i in range(steps):
        val = int(50 * (1 - i / steps))  # aaand back to blue
        rgb.set_rgb_value(0, (0, 0, val))
        rgb.set_rgb_value(1, (0, 0, val))
        time.sleep(0.01)
