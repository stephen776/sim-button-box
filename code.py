import time
import board
import digitalio
import usb_hid
import rotaryio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_debouncer import Debouncer

# ACC is finicky about timing of press and release of keyboard shortcut events so we will add an artificial delay in between
keyboard_event_delay_seconds=0.1

# buttons
keypress_pins = [board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11, board.GP12, board.GP13]
# array of debouncer objects
buttons = []

# Make all pin objects inputs with pull DOWNs (thus keypress = HIGH)
for pin in keypress_pins:
    key_pin = digitalio.DigitalInOut(pin)
    key_pin.direction = digitalio.Direction.INPUT
    key_pin.pull = digitalio.Pull.UP
    buttons.append(Debouncer(key_pin))
    
# keyboard
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
kbd = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(kbd)  # We're in the US :)

# encoders
encoder1 = rotaryio.IncrementalEncoder(board.GP20, board.GP21)
encoder2 = rotaryio.IncrementalEncoder(board.GP18, board.GP19)
encoder3 = rotaryio.IncrementalEncoder(board.GP16, board.GP17)
encoder4 = rotaryio.IncrementalEncoder(board.GP14, board.GP15)

# Store previous encoder positions to detect changes
last_position1 = encoder1.position
last_position2 = encoder2.position
last_position3 = encoder3.position
last_position4 = encoder4.position

def check_encoder_1():
    current_position1 = encoder1.position
    if current_position1 < last_position1:
        increase_bb()
    elif current_position1 > last_position1:
        decrease_bb()
    return current_position1

def check_encoder_2():
    current_position2 = encoder2.position
    if current_position2 < last_position2:
        increase_engine_map()
    elif current_position2 > last_position2:
        decrease_engine_map()
    return current_position2

def check_encoder_3():
    current_position3 = encoder3.position
    if current_position3 < last_position3:
        increase_abs()
    elif current_position3 > last_position3:
        decrease_abs()
    return current_position3

def check_encoder_4():
    current_position4 = encoder4.position
    if current_position4 < last_position4:
        increase_tc()
    elif current_position4 > last_position4:
        decrease_tc()
    return current_position4

# acc shortcuts
def ignition():
    kbd.press(Keycode.SHIFT)
    kbd.press(Keycode.I)
    time.sleep(keyboard_event_delay_seconds) 
    kbd.release(Keycode.I)
    kbd.release(Keycode.SHIFT)
    return

def starter():
    kbd.press(Keycode.S)
    time.sleep(2) # starter needs a longer hold but I don't wanna mess with separate press/release events for this one off case
    kbd.release(Keycode.S)
    return

def wiper():
    kbd.press(Keycode.ALT)
    kbd.press(Keycode.R)
    time.sleep(keyboard_event_delay_seconds)
    kbd.release(Keycode.R)
    kbd.release(Keycode.ALT)
    return

def toggle_lights():
    kbd.press(Keycode.L)
    time.sleep(keyboard_event_delay_seconds)
    kbd.release(Keycode.L)
    return

def toggle_rain_lights():
    kbd.press(Keycode.CONTROL)
    kbd.press(Keycode.L)
    time.sleep(keyboard_event_delay_seconds)
    kbd.release(Keycode.L)
    kbd.release(Keycode.CONTROL)
    return

def toggle_flashing_lights():
    kbd.press(Keycode.SHIFT)
    kbd.press(Keycode.L)
    time.sleep(keyboard_event_delay_seconds)
    kbd.release(Keycode.L)
    kbd.release(Keycode.SHIFT)
    return

def engage_pit_limiter():
    kbd.press(Keycode.ALT)
    kbd.press(Keycode.L)
    time.sleep(keyboard_event_delay_seconds)
    kbd.release(Keycode.L)
    kbd.release(Keycode.ALT)
    return

def cycle_racelogic():
    kbd.press(Keycode.ALT)
    kbd.press(Keycode.D)
    time.sleep(keyboard_event_delay_seconds)
    kbd.release(Keycode.D)
    kbd.release(Keycode.ALT)
    return

def increase_abs():
    kbd.press(Keycode.SHIFT)
    kbd.press(Keycode.A)
    time.sleep(keyboard_event_delay_seconds)
    kbd.release(Keycode.A)
    kbd.release(Keycode.SHIFT)
    return

def decrease_abs():
    kbd.press(Keycode.CONTROL)
    kbd.press(Keycode.A)
    time.sleep(keyboard_event_delay_seconds)
    kbd.release(Keycode.A)
    kbd.release(Keycode.CONTROL)
    return

def increase_tc():
    kbd.press(Keycode.SHIFT)
    kbd.press(Keycode.T)
    time.sleep(keyboard_event_delay_seconds)
    kbd.release(Keycode.T)
    kbd.release(Keycode.SHIFT)
    return

def decrease_tc():
    kbd.press(Keycode.CONTROL)
    kbd.press(Keycode.T)
    time.sleep(keyboard_event_delay_seconds)
    kbd.release(Keycode.T)
    kbd.release(Keycode.CONTROL)
    return

def increase_bb():
    kbd.press(Keycode.SHIFT)
    kbd.press(Keycode.B)
    time.sleep(keyboard_event_delay_seconds)
    kbd.release(Keycode.B)
    kbd.release(Keycode.SHIFT)
    return

def decrease_bb():
    kbd.press(Keycode.CONTROL)
    kbd.press(Keycode.B)
    time.sleep(keyboard_event_delay_seconds)
    kbd.release(Keycode.B)
    kbd.release(Keycode.CONTROL)
    return

def increase_engine_map():
    kbd.press(Keycode.SHIFT)
    kbd.press(Keycode.E)
    time.sleep(keyboard_event_delay_seconds)
    kbd.release(Keycode.E)
    kbd.release(Keycode.SHIFT)
    return

def decrease_engine_map():
    kbd.press(Keycode.CONTROL)
    kbd.press(Keycode.E)
    time.sleep(keyboard_event_delay_seconds)
    kbd.release(Keycode.E)
    kbd.release(Keycode.CONTROL)
    return

def cycle_camera():
    kbd.press(Keycode.F1)
    time.sleep(keyboard_event_delay_seconds)
    kbd.release(Keycode.F1)
    return

def not_mapped():
    return

button_map = {
    0: ignition,
    1: starter,
    2: engage_pit_limiter,
    3: cycle_racelogic,
    4: toggle_lights,
    5: wiper,
    6: toggle_flashing_lights,
    7: cycle_camera,
    8: toggle_rain_lights,
    9: not_mapped,
    10: not_mapped,
    11: not_mapped,
    12: not_mapped,
    13: not_mapped
}


while True:
    # check buttons
    for i in range(len(buttons)):
        button = buttons[i]
        button.update()
        if button.fell:
            button_map[i]()


    #check encoders
    last_position1 = check_encoder_1()
    last_position2 = check_encoder_2()
    last_position3 = check_encoder_3()
    last_position4 = check_encoder_4()

