import matplotlib.pyplot as plt
import math
import config

plt.ion()  # Interactive mode on for live update

# To store the history of target positions
target_history = []

# Define robot link lengths 
LINK_LENGTHS = [config.L, config.L, config.L]


def update_visualization(joint_angles, target_pos, task_label=None):
    global target_history

    # Append current target position to history
    target_history.append(target_pos)

    # Clear previous plot
    plt.clf()
    ax = plt.gca()

    # Plot target trajectory as green line
    xs_traj, ys_traj = zip(*target_history)
    ax.plot(xs_traj, ys_traj, 'g-', label='Target Trajectory')

    # Calculate robot joint positions from angles
    x, y = 0, 0
    xs, ys = [x], [y]
    angle = 0

    for theta, length in zip(joint_angles, LINK_LENGTHS):
        angle += theta
        x += length * math.cos(angle)
        y += length * math.sin(angle)
        xs.append(x)
        ys.append(y)

     # end-effector offset (rotated by total angle)
    offset_x = config.EE_offset[0] * math.cos(angle) - config.EE_offset[1] * math.sin(angle)
    offset_y = config.EE_offset[0] * math.sin(angle) + config.EE_offset[1] * math.cos(angle)

    ee_x = xs[-1] + offset_x
    ee_y = ys[-1] + offset_y

    # Plot robot arm links and joints
    ax.plot(xs, ys, 'o-', label='Robot Arm')

    # Highlight end effector with a blue dot at the correct position including offset
    ax.plot(ee_x, ee_y, 'bo', markersize=8, label='End-Effector')


    # Plot current target as a green star
    ax.plot(target_pos[0], target_pos[1], 'g*', markersize=8, label='Current Target')

    # Draw restricted area as red dashed circle only if enabled
    if config.ENABLE_RESTRICTED_AREA:
        restricted_circle = plt.Circle(
            config.RESTRICTED_AREA_CENTER,
            config.RESTRICTED_AREA_RADIUS,
            color='red',
            fill=False,
            linestyle='--',
            label='Restricted Area'
        )
        ax.add_patch(restricted_circle)

    # Set plot limits and aspect ratio
    reach = sum(LINK_LENGTHS) + 0.5 # to account for end_effector
    ax.set_xlim(-reach, reach)
    ax.set_ylim(-reach, reach)
    ax.set_aspect('equal')
    ax.grid(True)
    ax.legend(loc='upper right')

    # Pause briefly to update the plot
    plt.pause(0.001)
