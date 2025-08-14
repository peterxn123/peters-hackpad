import digitalio
import microcontroller
import board
import time


from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.scanners.encoder import RotaryioEncoder
from kmk.extensions.rgb import RGB
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler

keyboard = KMKKeyboard()
keyboard.matrix = [
    KeysScanner(
        pins=[
            board.A0,                       # GPIO26
            board.A1,                       # GPIO27
            board.A2,                       # GPIO28
            board.A3,                       # GPIO29
            board.D7,                       # GPIO7
            microcontroller.pin.GPIO0,      # GPIO0
            microcontroller.pin.GPIO4       # Encoder button S1
        ],
        value_when_pressed=False,
        pull=True
    ),
    RotaryioEncoder(
        pin_a=microcontroller.pin.GPIO2,
        pin_b=microcontroller.pin.GPIO1
    )
]

keyboard.coord_mapping = [0, 1, 2, 3, 4, 5, 6]

rgb = RGB(
    pixel_pin=microcontroller.pin.GPIO6,
    num_pixels=2,
    rgb_order=(1, 0, 2),
    brightness_limit=255,
)
keyboard.extensions.append(rgb)

encoder_handler = EncoderHandler()
encoder_handler.encoder_map = [
    ((KC.VOLD, KC.VOLU),)
]
keyboard.modules.append(encoder_handler)

keyboard.keymap = [
    [
        KC.LGUI(KC.D),
        KC.LGUI(KC.TAB),
        KC.LGUI(KC.L),
        KC.LGUI(KC.E),
        KC.LCTL(KC.C),
        KC.LCTL(KC.V),
        KC.ENTER
    ]
]


@keyboard.on_startup
def set_initial_leds():
    base_color = (0, 0, 50)
    rgb.set_rgb_value(0, base_color)
    rgb.set_rgb_value(1, base_color)


@keyboard.on_key
def animate_on_key(key, pressed, **kwargs):
    if pressed:
        pulse_animation()


def pulse_animation():
    steps = 10
    for i in range(steps):
        val = int(255 * (i / steps))
        rgb.set_rgb_value(0, (val, val, val))
        rgb.set_rgb_value(1, (val, val, val))
        time.sleep(0.01)

    for i in range(steps):
        val = int(50 * (1 - i / steps))
        rgb.set_rgb_value(0, (0, 0, val))
        rgb.set_rgb_value(1, (0, 0, val))
        time.sleep(0.01)


if __name__ == '__main__':
    keyboard.go()
