import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

## INPUT
x_pos = ctrl.Antecedent(np.arange(-1000, 2001, 1), 'posX') # Odległość od centrum domyślnej planszy, gdzie 0 to lewa krawędź a 1000 to prawa
y_pos = ctrl.Antecedent(np.arange(-1000, 1001, 1), 'posY') # Wysokość od gruntu planszy, gdzie 1000 to grunt, a 0 to górna krawędź planszy
angle = ctrl.Antecedent(np.arange(-179, 181, 1), 'angle') # Kąt natarcie gdzie 0 to wertykalny z nogami na dół, ujemne to wychylenie dołem w prawo a dodatnie to wychylenie dołem w lewo
y_velocity = ctrl.Antecedent(np.arange(-50, 51, 1), 'velocityY')  # Prędkość wertykalna - ujemne to lot w górę, dodatnie to lot w dół
x_velocity = ctrl.Antecedent(np.arange(-50, 51, 1), 'velocityX')  # Prędkość horyzontalna - dodatnie to lot w prawo, ujemne to lot w lewo

## OUTPUT
deltaAngle = ctrl.Consequent(np.arange(-3,4, 0.25), 'deltaAngle') # Jak bardzo należy zmienić kąt w tej iteracji?
thrustControl = ctrl.Consequent(np.arange(0,0.3, 0.05), 'thrustControl') # Jak bardzo należy wzmocnić napęd w tej iteracji?

## FUZZY MEMBERSHIP FUNCTIONS - inputs
### x_pos
x_pos['far_left'] = fuzz.trimf(x_pos.universe, [-1000, -1000, 100])
x_pos['left'] = fuzz.trimf(x_pos.universe, [0, 0, 300])

x_pos['optimal'] = fuzz.trimf(x_pos.universe, [250, 500, 750])

x_pos['right'] = fuzz.trimf(x_pos.universe, [700, 1000, 1000])
x_pos['far_right'] = fuzz.trimf(x_pos.universe, [900, 2000, 2000])

### y_pos
y_pos['too_high_altitude'] = fuzz.trimf(y_pos.universe, [-1000, -1000, 0])
y_pos['high_altitude'] = fuzz.trimf(y_pos.universe, [0, 0, 300])
y_pos['medium_altitude'] = fuzz.trimf(y_pos.universe, [300, 500, 600])
y_pos['low_altitude'] = fuzz.trimf(y_pos.universe, [600, 1000, 1000])

### angle
angle['optimal'] = fuzz.trimf(angle.universe,[-30, 0, 30])

angle['left'] = fuzz.trimf(angle.universe,[0, 179, 179])
angle['right'] = fuzz.trimf(angle.universe,[-179, -179, 0])

angle['slight_left'] = fuzz.trimf(angle.universe,[0, 30, 30])
angle['slight_right'] = fuzz.trimf(angle.universe,[-30, -30, 0])

angle['dangerous_left'] = fuzz.trimf(angle.universe,[30, 89, 89])
angle['dangerous_right'] = fuzz.trimf(angle.universe,[-89, -89, -30])

angle['extreme_left'] = fuzz.trimf(angle.universe,[89, 180, 180])
angle['extreme_right'] = fuzz.trimf(angle.universe,[-179, -179, -89])

### y_velocity
y_velocity['escape_velocity'] = fuzz.trimf(y_velocity.universe,[-1, -1, 0])
y_velocity['too_low'] = fuzz.trimf(y_velocity.universe, [-1, -1, 0.4])

y_velocity['optimal'] = fuzz.trimf(y_velocity.universe,[0.1, 0.5, 0.5])

y_velocity['bit_high'] = fuzz.trimf(y_velocity.universe,[0.4, 1, 1])
y_velocity['too_high'] = fuzz.trimf(y_velocity.universe,[0.5, 50, 50])

### x_velocity
# x_velocity['optimal'] = fuzz.trimf(x_velocity.universe,[-0.5, 0, 0.5])
#
# x_velocity['too_left'] = fuzz.trimf(x_velocity.universe,[0.4, 50, 50])
# x_velocity['too_right'] = fuzz.trimf(x_velocity.universe,[-50, -50, -0.4])

# x_velocity['extreme_left'] = fuzz.trimf(x_velocity.universe,[2, 50, 50])
# x_velocity['extreme_right'] = fuzz.trimf(x_velocity.universe,[-50, -50, -2])

## FUZZY MEMBERSHIP FUNCTIONS - outputs
### deltaAngle
deltaAngle['slight_left'] = fuzz.trimf(deltaAngle.universe, [0, 0.25, 1])
deltaAngle['slight_right'] = fuzz.trimf(deltaAngle.universe, [-1, -0.25, 0])

deltaAngle['left'] = fuzz.trimf(deltaAngle.universe, [0, 3, 3])
deltaAngle['right'] = fuzz.trimf(deltaAngle.universe, [-3, -3, 0])

### thrustControl
thrustControl['less_thrust'] = fuzz.trimf(thrustControl.universe, [0, 0, 0.1])
thrustControl['thrust_shutdown'] = fuzz.trimf(thrustControl.universe, [-1, -1, 0])
thrustControl['slight_thrust'] = fuzz.trimf(thrustControl.universe, [-0.2, 0.05, 0.2])
thrustControl['medium_thrust'] = fuzz.trimf(thrustControl.universe, [-0.05, 0.12, 0.3])
thrustControl['strong_thrust'] = fuzz.trimf(thrustControl.universe, [0.0, 0.16, 0.30])

## RULES
correct_left = ctrl.Rule(angle['left'], deltaAngle['slight_right'])
correct_right = ctrl.Rule(angle['right'], deltaAngle['slight_left'])

# allow_going_down = ctrl.Rule(y_velocity['optimal'], thrustControl['no_thrust'])
speed_down_medium_alt = ctrl.Rule(y_pos['medium_altitude'] & angle['optimal'], thrustControl['medium_thrust'])
speed_down_near_ground = ctrl.Rule(y_pos['low_altitude'] & angle['optimal'], thrustControl['strong_thrust'])
respond_to_extreme_velocity = ctrl.Rule(y_velocity['too_high'] & angle['optimal'], thrustControl['slight_thrust'])
dont_reverse_direction = ctrl.Rule(y_velocity['too_low'] & angle['optimal'], thrustControl['less_thrust'])
dont_go_up = ctrl.Rule(y_velocity['escape_velocity'], thrustControl['thrust_shutdown'])

landing_ctrl = ctrl.ControlSystem(
     [correct_left, correct_right, speed_down_medium_alt, speed_down_near_ground, respond_to_extreme_velocity, dont_reverse_direction, dont_go_up]
    )

landing_sim = ctrl.ControlSystemSimulation(landing_ctrl)