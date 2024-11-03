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
y_velocity['escape_velocity'] = fuzz.trimf(y_velocity.universe,[-50, -50, 0])

y_velocity['optimal'] = fuzz.trimf(y_velocity.universe,[0, 0.1, 0.5])

y_velocity['bit_high'] = fuzz.trimf(y_velocity.universe,[0.4, 1, 1])
y_velocity['too_high'] = fuzz.trimf(y_velocity.universe,[0.5, 50, 50])

### x_velocity
x_velocity['optimal'] = fuzz.trimf(x_velocity.universe,[-0.5, 0, 0.5])

x_velocity['too_left'] = fuzz.trimf(x_velocity.universe,[0.4, 50, 50])
x_velocity['too_right'] = fuzz.trimf(x_velocity.universe,[-50, -50, -0.4])

x_velocity['extreme_left'] = fuzz.trimf(x_velocity.universe,[2, 50, 50])
x_velocity['extreme_right'] = fuzz.trimf(x_velocity.universe,[-50, -50, -2])

## FUZZY MEMBERSHIP FUNCTIONS - outputs
### deltaAngle
deltaAngle['slight_left'] = fuzz.trimf(deltaAngle.universe, [0, 0.25, 1])
deltaAngle['slight_right'] = fuzz.trimf(deltaAngle.universe, [-1, -0.25, 0])

deltaAngle['left'] = fuzz.trimf(deltaAngle.universe, [0, 3, 3])
deltaAngle['right'] = fuzz.trimf(deltaAngle.universe, [-3, -3, 0])

### thrustControl
thrustControl['no_thrust'] = fuzz.trimf(thrustControl.universe, [0, 0, 0.1])
thrustControl['slight_thrust'] = fuzz.trimf(thrustControl.universe, [0, 0.1, 0.2])
thrustControl['strong_thrust'] = fuzz.trimf(thrustControl.universe, [0.1, 0.3, 0.3])

## RULES
## 1. y_velocity too high
rule_1a = ctrl.Rule(y_velocity['too_high'] & angle['optimal'], thrustControl['strong_thrust'])
rule_1b_angle = ctrl.Rule(y_velocity['too_high'] & angle['left'], deltaAngle['slight_right'])
rule_1b_thrust = ctrl.Rule(y_velocity['too_high'] & angle['left'], thrustControl['slight_thrust'])
rule_1c_angle = ctrl.Rule(y_velocity['too_high'] & angle['right'], deltaAngle['slight_left'])
rule_1c_thrust = ctrl.Rule(y_velocity['too_high'] & angle['right'], thrustControl['slight_thrust'])

rule_1d1_angle = ctrl.Rule(y_velocity['too_high'] & angle['extreme_left'], deltaAngle['right'])
rule_1d1_thrust = ctrl.Rule(y_velocity['too_high'] & angle['extreme_left'], thrustControl['no_thrust'])
rule_1d2_angle = ctrl.Rule(y_velocity['too_high'] & angle['extreme_right'], deltaAngle['left'])
rule_1d2_thrust = ctrl.Rule(y_velocity['too_high'] & angle['extreme_right'], thrustControl['no_thrust'])

## 2. Dangerous angle
rule_2a = ctrl.Rule(angle['dangerous_left'], deltaAngle['slight_right'])
rule_2b = ctrl.Rule(angle['dangerous_right'], deltaAngle['slight_left'])

rule_2c = ctrl.Rule(angle['extreme_left'], deltaAngle['right'])
rule_2d = ctrl.Rule(angle['extreme_right'], deltaAngle['left'])

## 3. Ship too far away from the center of the map
rule_3a_angle = ctrl.Rule(x_pos['left'], deltaAngle['slight_right'])
rule_3a_thrust = ctrl.Rule(x_pos['left'], thrustControl['slight_thrust'])
rule_3b_angle = ctrl.Rule(x_pos['right'], deltaAngle['slight_left'])
rule_3b_thrust = ctrl.Rule(x_pos['right'], thrustControl['slight_thrust'])

rule_3c_angle = ctrl.Rule(x_pos['far_left'], deltaAngle['right'])
rule_3c_thrust = ctrl.Rule(x_pos['far_left'], thrustControl['slight_thrust'])
rule_3d_angle = ctrl.Rule(x_pos['far_right'], deltaAngle['left'])
rule_3d_thrust = ctrl.Rule(x_pos['far_right'], thrustControl['slight_thrust'])

## 4. Ship goes too much to the side
rule_4a = ctrl.Rule(x_velocity['extreme_left'], deltaAngle['right'])
rule_4b = ctrl.Rule(x_velocity['extreme_right'], deltaAngle['left'])

rule_4a_angle = ctrl.Rule(x_velocity['too_left'], deltaAngle['right'])
rule_4a_thrust = ctrl.Rule(x_velocity['too_left'], thrustControl['slight_thrust'])
rule_4b_angle = ctrl.Rule(x_velocity['too_right'], deltaAngle['left'])
rule_4b_thrust = ctrl.Rule(x_velocity['too_right'], thrustControl['slight_thrust'])

## 5. y_velocity < 0
rule_5 = ctrl.Rule(y_velocity['escape_velocity'], thrustControl['no_thrust'])

## Create a control system and simulation
landing_ctrl = ctrl.ControlSystem(
     [rule_1a, rule_1b_angle, rule_1b_thrust, rule_1c_angle, rule_1c_thrust, rule_1d1_angle, rule_1d1_thrust, \
      rule_1d2_angle, rule_1d2_thrust, rule_2a, rule_2b, rule_2c, rule_2d, rule_3a_angle, rule_3a_thrust, \
      rule_3b_angle, rule_3b_thrust, rule_3c_angle, rule_3c_thrust, rule_3d_angle, rule_3d_thrust, rule_4a, rule_4b, \
      rule_5]
    )

landing_sim = ctrl.ControlSystemSimulation(landing_ctrl)