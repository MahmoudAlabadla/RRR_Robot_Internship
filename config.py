# config.py
import math

# General settings

# Define L (sine-wave and robot links) can be set to a random number (try changing to see impact on simulation)
L = 2.5  # represents L and Links length


# For Task A
TASK = 'A'  # or 'B'

if TASK == 'A':
    f = 30  # Target position frequency 30Hz
    TARGET_UPDATE_HZ = 30       # same as f 
    CONTROL_LOOP_HZ = 1000
elif TASK == 'B':
    f = 5   # Target position frequency 5Hz
    TARGET_UPDATE_HZ = 5        # same as f 
    CONTROL_LOOP_HZ = 50

# Additional Tasks
ENABLE_RESTRICTED_AREA = False  # False for Task A, True for Task B

# Toggle for enabling/disabling joint angle restriction
ENABLE_JOINT_LIMITS = True     # Additional features

# Restricted area parameters (used if ENABLE_RESTRICTED_AREA=True)
RESTRICTED_AREA_CENTER = (2* L, 0.5 * L)
RESTRICTED_AREA_RADIUS = L / 8

#Define End_effector Offset
EE_offset = [0.2, 0, 0] # along the x-axis

# Joint angle limits: (min, max) for each joint in degrees, adjust to see impact on simulation
JOINT_LIMITS = [
    (-math.radians(10), math.radians(10)),   # Joint 1 (base) – slightly more than ±90°
    (-math.radians(15), math.radians(15)),   # Joint 2 – more flexible
    (-math.radians(5), math.radians(5)),   # Joint 3 – even more flexible
]

