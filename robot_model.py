import tinyik #Using the tinyik library for robot desgin and kinematics
import numpy as np
import config
from config import EE_offset

#Define link length
L = config.L # Random selection for now


#Define the Robot (Rotation around 'z' )
robot = tinyik.Actuator([
    'z', L,   # First joint 
    'z', L,   # Second joint
    'z', L ,   # Third joint
    EE_offset  # End_effector Offset
])

def clamp_angles(angles):
    """
    Clamp each joint angle within its predefined limits.

    Parameters:
    angles (list or iterable): List of joint angles (in radians) to be clamped.

    Returns:
    list: A list of clamped joint angles, where each angle is restricted 
          between its corresponding min and max limits defined in config.JOINT_LIMITS.
    """
    clamped = []
    for angle, (min_limit, max_limit) in zip(angles, config.JOINT_LIMITS):
        # Clamp the angle so it does not go below min_limit or above max_limit
        clamped.append(max(min(angle, max_limit), min_limit))
    return clamped

#Function to return the inverse kinematics given updated x, y coordinates of the target 
def get_joint_angles (target_pose):

    """
    This Function, computes the joint angles to reach current target position. 
    
    Input is a tuple of x, y

    Output is a list of joint angles in radians

    """
    x, y = target_pose

    # for a 2d planar robot, z = 0
    try:
        robot.ee = [x, y, 0.0]      #Inverse Kinematics      # library expects 3D plane, hence z value
        angles = robot.angles
    
        if config.ENABLE_JOINT_LIMITS:
         angles = clamp_angles(angles)

        return angles # clamped angles are returned to be used and not the original IK angles


    except ValueError as e:
       print(f"Target {target_pose} is unreachable: {e}" )
       return None
    




