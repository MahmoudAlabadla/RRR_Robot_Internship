#controller.py

import math
import time
import config


# Define restricted circle size and location
radius = config.RESTRICTED_AREA_RADIUS
center_pos = config.RESTRICTED_AREA_CENTER


# Store starting time to compute t
start_time = time.time()

#def restrict_to_bounds(value, min_val, max_val):
#    return max(min_val, min(value, max_val))

def check_target_location(x, y):
    dx = x - center_pos[0]
    dy = y - center_pos[1]
    dist = math.sqrt(dx*dx + dy*dy)

    if dist >= radius:
        return x, y
    else:
        return closest_point_on_circle(x, y)

def closest_point_on_circle(x, y):
    dx = x - center_pos[0]
    dy = y - center_pos[1]
    dist = math.sqrt(dx*dx + dy*dy)

    if dist == 0:
        return center_pos[0] + radius, center_pos[1]

    scale = radius / dist
    closest_x = center_pos[0] + dx * scale
    closest_y = center_pos[1] + dy * scale
    return closest_x, closest_y

def update_target_position():
    """
    Returns:
        raw_target_pos: theoretical target position at current time
        ik_target_pos: adjusted position outside restricted area
    """
    # Elapsed time since program started
    t = time.time() - start_time

    # Theoretical trajectory
    x = 2 * config.L
    y = config.L * math.sin(2 * math.pi * config.f * t)

    # Optional bounds limiting
    # x = restrict_to_bounds(x, config.BOUNDS[0], config.BOUNDS[1])
    # y = restrict_to_bounds(y, config.BOUNDS[0], config.BOUNDS[1])

    raw_target_pos = (x, y) 
    # Apply restricted area check only if enabled
    if config.ENABLE_RESTRICTED_AREA:
        adjusted_target_pos = check_target_location(x, y)
    else:
        adjusted_target_pos = raw_target_pos


    return raw_target_pos, adjusted_target_pos
