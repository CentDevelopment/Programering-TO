import machine
import neopixel
import time

np = neopixel.NeoPixel(machine.Pin(14), 8)
pot = machine.ADC(26)
button_color = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_direction = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_DOWN)

colors = [
    (255, 0, 0),
    (255, 255, 0),
    (0, 255, 0),
    (0, 255, 255),
    (0, 0, 255),
    (255, 0, 255),
    (255, 255, 255)
]

color_index = 0
current_color = colors[color_index]
direction = 1
position = 0
last_button_color_state = 0
last_button_direction_state = 0
debounce_time = 200
last_press_time = 0

def get_speed_from_pot():
    pot_value = pot.read_u16()
    return max(20, int(300 - (pot_value / 65535 * 280)))

def change_color():
    global color_index, current_color
    color_index = (color_index + 1) % len(colors)
    current_color = colors[color_index]

def toggle_direction():
    global direction
    direction = -1 if direction == 1 else 1

def update_ring(position):
    np.fill((0, 0, 0))
    np[position] = current_color

    trailing_factors = [0.7, 0.5, 0.3, 0.2, 0.1]
    for i, factor in enumerate(trailing_factors):
        trailing_pos = (position - (i + 1) * direction) % 8
        np[trailing_pos] = (
            int(current_color[0] * factor),
            int(current_color[1] * factor),
            int(current_color[2] * factor)
        )
    
    np.write()

try:
    while True:
        speed = get_speed_from_pot()

        if button_color.value() == 1 and last_button_color_state == 0:
            change_color()
            time.sleep_ms(debounce_time)
        last_button_color_state = button_color.value()

        current_time = time.ticks_ms()
        if button_direction.value() == 1 and last_button_direction_state == 0:
            if time.ticks_diff(current_time, last_press_time) > debounce_time:
                toggle_direction()
                last_press_time = current_time
        last_button_direction_state = button_direction.value()

        position = (position + direction) % 8
        update_ring(position)
        time.sleep_ms(speed)

except KeyboardInterrupt:
    np.fill((0, 0, 0))
    np.write()
