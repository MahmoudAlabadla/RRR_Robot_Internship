import math
import time
import config


# Define restricted circle size and location
radius = config.RESTRICTED_AREA_RADIUS
center_pos = config.RESTRICTED_AREA_CENTER

# Store starting time to compute t
start_time = time.time()

def check_target_location(x, y):
    """
    Checks if the given point (x, y) is outside the restricted circle.
    If inside, returns the closest point on the circle boundary instead.

    Args:
        x (float): x-coordinate of the target
        y (float): y-coordinate of the target

    Returns:
        tuple: adjusted (x, y) position respecting the restricted area
    """
    dx = x - center_pos[0]
    dy = y - center_pos[1]
    dist = math.sqrt(dx*dx + dy*dy)

    if dist >= radius:
        # Target is outside restricted area, return as is
        return x, y
    else:
         # Target is inside restricted area, clamp to circle edge
        return closest_point_on_circle(x, y)

def closest_point_on_circle(x, y):
    """
    Computes the closest point on the circumference of the restricted circle
    from the given point (x, y).

    Args:
        x (float): x-coordinate of the target inside restricted area
        y (float): y-coordinate of the target inside restricted area

    Returns:
        tuple: (x, y) coordinates on the circle edge closest to the input point
    """
    dx = x - center_pos[0]
    dy = y - center_pos[1]
    dist = math.sqrt(dx*dx + dy*dy)

    if dist == 0:
        # If exactly at the center, return a point on the circle along positive x-axis
        return center_pos[0] + radius, center_pos[1]

    # Scale vector from center to point to the radius length
    scale = radius / dist
    closest_x = center_pos[0] + dx * scale
    closest_y = center_pos[1] + dy * scale
    return closest_x, closest_y

def update_target_position():
    """
    Computes the current theoretical target position following a sinusoidal trajectory,
    and adjusts it if it lies within a restricted circular area.

    Returns:
        raw_target_pos (tuple): theoretical target position without restrictions
        ik_target_pos (tuple): adjusted target position respecting restricted area
    """
    # Elapsed time since program started
    t = time.time() - start_time

      # Theoretical trajectory: fixed x, sinusoidal y movement
    x = 2 * config.L
    y = config.L * math.sin(2 * math.pi * config.f * t)

    raw_target_pos = (x, y) 
    
    # Apply restricted area constraint only if enabled in config
    if config.ENABLE_RESTRICTED_AREA:
        adjusted_target_pos = check_target_location(x, y)
    else:
        adjusted_target_pos = raw_target_pos


    return raw_target_pos, adjusted_target_pos
