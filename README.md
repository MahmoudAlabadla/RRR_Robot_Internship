This project simulates a 3-DOF planar RRR robot that tracks a moving 2D target in real-time using inverse kinematics. The system supports configurable tasks, obstacle zone, and joint limits, all visualized using matplotlib. Designed with a modular layered architecture to ensure clarity, flexibility, and extensibility.

Observations between Task A, Task B, restricted area, and joint limits

In Task A, the target (marked as a green star) jumps around really fast—30 times a second—so the robot has to keep up with quick movements.

In Task B, both the target and the robot update slower, making the whole simulation feel smoother and less jumpy.

Adding the restricted circular area shows up nicely as a red circle on the screen. The target moves freely inside it, but the robot’s end-effector doesn’t go inside—it stays right on the edge.

Turning on joint limits can affect whether the robot can actually reach the target. When the limits are set realistically, everything works fine. But if the limits are too tight (like only ±50 degrees), the robot might not be able to get to some spots.



Documentation:

1-  Instruction for recreating project simulation:

    A)  Clone the Repository
        Clone this repository from your lab code remote:

        git clone "https://github.com/MahmoudAlabadla/RRR_Robot_Internship.git
        cd "labcode-repo"

    B)  Create and activate a virtual environment (optional but recommended)

        python3 -m venv venv
        source venv/bin/activate

    C) Install required packages 

        pip install -r requirements.txt

        - OR manually

        pip install tinyik matplotlib numpy

    D) Open config.py in your code editor

        Set TASK = 'A'  # or 'B'

        Additionally, set 

            ENABLE_RESTRICTED_AREA = True

            ENABLE_JOINT_LIMITS = True 

            adjust JOINT_LIMITS to see effect on simulation

    E) run the follwoing commad in your terminal 
            
            python main.py

    "The simulation does not require any external input files. All target motion and configurations are generated programmatically."




2-	Description of Modular approach (layered architecture)

    For this project, we followed a layered arciticture approach to promote modulaity, abstraction and easier testing, with layer having a clear responsability.

    A)  Application Layer
        In this layer, we have the main.py script acting as the orchestrator. Using a logical workflow, the main.py is able to 
        continuously simulated the RRR robot in real-time showing change of target location and reflecting the follow up of the end-effector. It implements main control loop, handles timing and coordination of data flow. It also abstracts the underlying control logic from the user.

    B)  Control Layer
        This layer includes the controller.py module. It is responsible for applying target trajectory, managing frequencies and applies motion constraints. This layer also adjusts the end-effector position if target enters restricted area.

    C)  Hardware Absraction Layer
        This layer is represented by robot_model.py, which implements the RRR robot using the TinyIK library. It handles the inverse kinematics (IK) and forwards joint commands to the simulated robot model. This layer serves as a bridge between high-level commands (from the controller) and low-level hardware (or simulated hardware), providing an abstraction from the underlying kinematics logic.

    D)  Configuration Layer
    
        To support flexibility and task-specific behavior, a separate config.py module is used. It contains all configurable parameters, including:

            - Control and target update frequencies

            - Link lengths and end-effector offsets

            - Restricted area parameters

            - Feature toggles like ENABLE_RESTRICTED_AREA and ENABLE_JOINT_LIMITS

        This allows seamless switching between tasks (e.g., Task A, Task B, or extended tasks) without modifying core logic.

    E) Visualization Layer

        The visualizer.py file represents the Visualization Layer, which is responsible for the real-time 2D plotting of the robot's configuration. This includes visualizing the positions of the robot’s joints and links, the current position of the end-effector (including its offset), and the trajectory of the moving target. It also renders any restricted areas, such as the red circular obstacle, when enabled in the configuration. This layer plays an essential role in monitoring and understanding the system’s behavior during simulation.
        Restricted region (if enabled)


3-	Modules

    A)  controller.py:
    Module Description:

    -   Function: update_target_position()
        Description:
        Calculates the current target's theoretical position based on a sine wave trajectory and adjusts it if it violates the restricted zone (if enabled).

        Inputs: None directly (relies on config parameters like f, L, and ENABLE_RESTRICTED_AREA)

        Outputs:

        raw_target_pos: tuple (x, y) of the unadjusted target

        ik_target_pos: tuple (x, y) adjusted to avoid restricted area

        Role:
        Supplies updated target positions at a defined frequency. It provides both the visual target and the adjusted one for inverse kinematics.


    -   Function: check_target_location(x, y)

        Description:
        Determines whether the target is inside the restricted circular area.

        Inputs:

        x, y: coordinates of the target

        Outputs:

        Tuple (x, y): either unchanged or modified to lie just outside the restricted area

        Role:
        Ensures the target avoids restricted areas by returning a legal position.


    -   Function: closest_point_on_circle(x, y)

        Description:
        Computes the closest point on the boundary of the restricted circle.

        Inputs:

        x, y: coordinates of a point inside the restricted area

        Outputs:

        Tuple (x, y) representing the nearest legal point on the circle's boundary

        Role:
        Supporting function for boundary enforcement in the check_target_location.


    B)  robot_model.py
    Module Description:

    -   Function: get_joint_angles(target_pose)

        Description:
        Computes the joint angles needed for the robot’s end-effector to reach a given target position in 2D space using inverse kinematics (via the tinyik library).

        Inputs:

        target_pose: A tuple (x, y) representing the desired position of the end-effector in 2D.

        Outputs:

        A list of joint angles [θ1, θ2, θ3] in radians, if the target is reachable.

        Returns None if the target is outside the robot's workspace and unreachable.

        Role in Program Flow:
        This function is called regularly from main.py to update the joint configuration based on the most recent target position. It is part of the robot’s “HAL” (Hardware Abstraction Layer) and is responsible for converting Cartesian coordinates into joint space angles.

    
    C)  visualizer.py
    Module Description:

    -   Function: update_visualization(joint_angles, target_pos)

        Description:
        Continuously updates the 2D visual representation of the robot's movement and target tracking in real time.

        Inputs:

        joint_angles: A list [θ1, θ2, θ3] representing the current angles of the robot’s joints in radians.

        target_pos: A tuple (x, y) representing the current target’s position in 2D space.

        Outputs:

        None (this function is purely visual and does not return any data).

        Role in Program Flow:
        Called in every control loop iteration from main.py, this function visualizes:

        The robot’s configuration (link positions based on joint angles)

        The position of the end-effector (including offset)

        The historical trajectory of the target (green path)

        The restricted area (if enabled) as a red dashed circle
        It uses Matplotlib to provide live feedback and debugging insight into how well the robot tracks the moving target.

    D) main.py
    Module Description:
        
        This is the main control loop of the program. It coordinates the update of the target position, computes inverse kinematics to find joint angles, and visualizes the robot in real-time. It runs continuously, maintaining update frequencies defined in config.py.

        Function Flow Summary:
        Loop Structure:

        Runs at a control frequency set by CONTROL_LOOP_HZ.

        Periodically updates the target position (based on TARGET_UPDATE_HZ).

        Uses inverse kinematics (via robot_model) to compute joint angles for the new target.

        Passes the joint angles and target position to visualizer.update_visualization() for real-time display.