import controller
import time
import robot_model
import visualizer
import config

# Initialization of loop frequencies from configuration
CONTROL_LOOP_HZ = config.CONTROL_LOOP_HZ
TARGET_UPDATE_HZ = config.TARGET_UPDATE_HZ

# Calculate time intervals for target updates and control loop delays
target_update_interval = 1.0 / TARGET_UPDATE_HZ
control_loop_interval = 1.0 / CONTROL_LOOP_HZ

# Track last target update time to control update frequency
last_update_time = time.time()

# Variables to store latest target position and joint angles
latest_target = None
latest_angles = None

# Main control loop - runs continuously at control loop frequency
while True: 
    current_time = time.time()  

    # Update target position and robot angles every 1/30 or  1/5 second
    if current_time - last_update_time >= target_update_interval:

        # Get new target poses for visualization and inverse kinematics
        visual_target_pose, ik_target_pose = controller.update_target_position()

        # Compute joint angles for new target position using inverse kinematics
        # Note: clamping of joint angles against limits is handled internally in get_joint_angles()
        latest_angles = robot_model.get_joint_angles(ik_target_pose)

        # Store the latest visual target for display
        latest_target = visual_target_pose
        # Reset timer after update
        last_update_time = current_time

    # Continuously update visualizer with the latest known positions (wait untill target moves)
    if latest_angles is not None and latest_target is not None: 
        visualizer.update_visualization(latest_angles, latest_target)
        

    # Sleep to maintain control loop frequency (set in configuration)
    time.sleep(control_loop_interval)