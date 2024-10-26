import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define fuzzy variables for inputs and outputs
## INPUTS
altitude = ctrl.Antecedent(np.arange(0, 101, 1), 'altitude')  # Altitude in arbitrary units - TODO: Integrate with game units
velocity = ctrl.Antecedent(np.arange(-50, 51, 1), 'velocity')  # Descent speed in arbitrary units - TODO: Integrate with game units
x_distance = ctrl.Antecedent(np.arange(-100, 101, 1), 'x_distance') # Distance on x-axis from the preferred landing spot. TODO: Might go well with log func?
## OUTPUTS
thrust = ctrl.Consequent(np.arange(0, 101, 1), 'thrust')  # Thrust power in arbitrary units - TODO: Integrate with game units
angle = ctrl.Consequent(np.arange(0,361, 1), 'angle') # Angle between ship and ground's horizon.

# Define fuzzy membership functions for altitude
altitude['low'] = fuzz.trimf(altitude.universe, [0, 0, 50])
altitude['medium'] = fuzz.trimf(altitude.universe, [0, 50, 100])
altitude['high'] = fuzz.trimf(altitude.universe, [50, 100, 100])

# Define fuzzy membership functions for velocity
velocity['fast'] = fuzz.trimf(velocity.universe, [-50, -50, 0])
velocity['moderate'] = fuzz.trimf(velocity.universe, [-50, 0, 50])
velocity['slow'] = fuzz.trimf(velocity.universe, [0, 50, 50])

# Define fuzzy membership functions for velocity
x_distance['far_left'] = fuzz.trimf(velocity.universe, [-100, -50, 0])
x_distance['slight_left'] = fuzz.trimf(velocity.universe, [-50, 0, 50])
x_distance['optimal'] = fuzz.trimf(velocity.universe, [0, 50, 50])
x_distance['slight_right'] = fuzz.trimf(velocity.universe, [-50, -50, 0])
x_distance['far_right'] = fuzz.trimf(velocity.universe, [-50, 0, 50])

# Define fuzzy membership functions for thrust
thrust['weak'] = fuzz.trimf(thrust.universe, [0, 0, 50])
thrust['average'] = fuzz.trimf(thrust.universe, [0, 50, 100])
thrust['strong'] = fuzz.trimf(thrust.universe, [50, 100, 100])

# Define fuzzy rules
## 1. When altitude is low, velocity should be low
rule1 = ctrl.Rule(altitude['low'], velocity['low'])
# rule1 = ctrl.Rule(altitude['low'] & velocity['slow'], thrust['low'])
rule2 = ctrl.Rule(altitude['low'] & velocity['fast'], thrust['high'])
rule3 = ctrl.Rule(altitude['medium'] & velocity['moderate'], thrust['medium'])
rule4 = ctrl.Rule(altitude['high'] & velocity['fast'], thrust['medium'])
rule5 = ctrl.Rule(altitude['high'] & velocity['slow'], thrust['low'])

# Create a control system and simulation
landing_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
landing_sim = ctrl.ControlSystemSimulation(landing_ctrl)

# Test the system with example inputs
landing_sim.input['altitude'] = 30  # For example, 30 units above surface
landing_sim.input['velocity'] = -20  # Descending at -20 units

# Compute the result
landing_sim.compute()

# Output the computed thrust
print("Suggested Thrust:", landing_sim.output['thrust'])
