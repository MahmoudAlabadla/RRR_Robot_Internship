# main.py
import controller
import time
import robot_model
import visualizer
import config

# Initialization
CONTROL_LOOP_HZ = config.CONTROL_LOOP_HZ
TARGET_UPDATE_HZ = config.TARGET_UPDATE_HZ
target_update_interval = 1.0 / TARGET_UPDATE_HZ
control_loop_interval = 1.0 / CONTROL_LOOP_HZ
last_update_time = time.time()

# Default values
latest_target = None
latest_angles = None

while True:  # loops at the desired task frequency (1000 or 50) set in config.py
    current_time = time.time()  

    # Update target position and robot angles every 1/30 or  1/5 second
    if current_time - last_update_time >= target_update_interval:
        visual_target_pose, ik_target_pose = controller.update_target_position()
        latest_angles = robot_model.get_joint_angles(ik_target_pose)
        latest_target = visual_target_pose
        last_update_time = current_time

    # Continuously update visualizer with the latest known positions (wait untill target moves)
    if latest_angles is not None and latest_target is not None: 
        visualizer.update_visualization(latest_angles, latest_target)
        

    # Sleep to maintain control loop frequency (set in configuration)
    time.sleep(control_loop_interval)