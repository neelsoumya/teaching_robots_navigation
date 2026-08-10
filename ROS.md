# ROS

- ROS system for robotics


Here is the complete introductory guide, operational principles, teaching notes, and educational resources for ROS 2 formatted in standard Markdown.

---

# Autonomous Mobile Robotics with ROS 2: Operating Principles, Architecture, and Educational Notes

## 1. Middleware Architecture and Operating Principles

The Robot Operating System (ROS 2) is an open-source middleware framework designed for real-time, distributed robotics engineering. Unlike traditional operating systems, ROS 2 runs as an abstraction layer on top of host operating systems such as Linux (Ubuntu), macOS, Windows, or real-time embedded environments.

```
+-------------------------------------------------------------+
|                 User Application / Nodes                    |
+-------------------------------------------------------------+
|    rclcpp (C++ Client Library) | rclpy (Python Client Library) |
+-------------------------------------------------------------+
|             RCL (ROS Client C Architecture)                 |
+-------------------------------------------------------------+
|               RMW (ROS Middleware Interface)                |
+-------------------------------------------------------------+
|            DDS (Data Distribution Service Layer)            |
+-------------------------------------------------------------+
|             Host Operating System (Linux / RTOS)            |
+-------------------------------------------------------------+

```

### Key Architectural Concepts

1. **Data Distribution Service (DDS) Middleware**: ROS 2 removes the single point of failure (the central `rosmaster` from ROS 1) by utilizing DDS, an industry standard for real-time peer-to-peer data transport.


2. **Dynamic Peer Discovery**: Nodes periodically broadcast their presence across local subnets using a specific domain identifier defined by the environment variable `ROS_DOMAIN_ID`. Nodes within the same domain automatically discover each other and establish direct peer-to-peer data links.


3. **Abstraction Layers**:
* **RMW (ROS Middleware Interface)**: Translates generic ROS message primitives into vendor-specific DDS implementations (such as eProsima Fast DDS or Eclipse Cyclone DDS).


* **RCL (ROS Client Library)**: A core C library providing foundational middleware APIs.


* **Language Client Libraries**: `rclcpp` (C++) and `rclpy` (Python) wrap RCL to provide language-native programming interfaces.




4. **Graph Isolation & Launch Automation**:
* **Namespaces**: Group nodes, topics, and services into isolated organizational paths (for example, `/robot1/` vs `/robot2/`) to prevent message collisions in multi-robot setups.


* **Launch System**: Python configuration scripts that automate launching multiple nodes, configuring dynamic parameters, and setting up environments in a single command.





---

## 2. Core Communication Primitives

At the center of ROS 2 is the **ROS Graph**, a dynamic network of computational units called **Nodes**. Each node should handle a single, modular responsibility (e.g., driver processing, state estimation, path planning). Nodes communicate using four primary mechanisms:

| Communication Primitive | Underlying Pattern | Execution Synchrony | Coupling Type | Data Flow | Canonical Robotics Use Case |
| --- | --- | --- | --- | --- | --- |
| **Topic** | Publish / Subscribe | Asynchronous | Fully Decoupled | Unidirectional (1-to-N, N-to-M) | Continuous sensor telemetry (`/scan`, `/odom`), raw velocity commands (`/cmd_vel`).

 |
| **Service** | Request / Response | Synchronous / Blocking | Temporally Coupled | Bidirectional Transaction | Rapid queries, toggling states, hardware recalibration, resetting odometry.

 |
| **Action** | Goal / Feedback / Result | Asynchronous / Non-Blocking | Loosely Coupled with Cancelability | Multichannel Bidirectional | Long-running tasks like driving to a goal pose (`/navigate_to_pose`).

 |
| **Parameter** | Key-Value Registry | Synchronous Read/Write | Node-Intrinsic | Local Configuration | Runtime adjustment of node settings, such as max velocity or sensor frame IDs.

 |

---

## 3. Kinematic Frame Transformations (REP 103 & REP 105)

Managing 3D dynamic coordinate frames is handled via the `tf2` transform library. Standard naming conventions and frame behaviors follow ROS Enhancement Proposals **REP 103** (Standard Units & Coordinate Axes: meters, radians, X-forward, Y-left, Z-up) and **REP 105** (Coordinate Frames for Mobile Platforms).

### Coordinate Frame Tree Hierarchy

```
   earth (Geodetic / Multi-robot anchor)
     |
    map (Global fixed reference, non-drifting, discrete updates)
     |
    odom (Local fixed reference, continuous, drifts over time)
     |
  base_link (Robot chassis origin / rotational center)
     |
  +-- base_laser (LiDAR sensor frame)
  +-- imu_link (Inertial measurement unit frame)

```

1. **`base_link`**: Rigidly attached to the robot base. Sensor transform offsets are defined relative to `base_link`.


2. **`odom`**: A world-fixed frame where the robot's pose is calculated via dead-reckoning (wheel encoders, visual odometry, IMU). The transform $T_{\text{odom} \to \text{base\_link}}$ is continuous and smooth, making it ideal for continuous motor control, but it drifts over time.


3. **`map`**: A world-fixed global reference frame. Algorithms like SLAM or Adaptive Monte Carlo Localization (AMCL) correct for odometric drift by matching real-time sensor observations to a global map.



### The Single-Parent Rule and Transform Factorization

`tf2` requires every frame to have **exactly one parent frame**. To support both continuous odometry and discrete global position corrections simultaneously without breaking the tree structure, authority is split:

* The odometry source publishes $T_{\text{odom} \to \text{base\_link}}$ continuously at a high update frequency (e.g., 100 Hz).


* The localization engine (AMCL or SLAM) computes the global position $T_{\text{map} \to \text{base\_link}}$ at a lower frequency (e.g., 1 Hz) and back-calculates $T_{\text{map} \to \text{odom}}$ using frame algebra:



$$T_{\text{map} \to \text{odom}} = T_{\text{map} \to \text{base\_link}} \cdot \left( T_{\text{odom} \to \text{base\_link}} \right)^{-1}$$

Discrete localization jumps are absorbed inside $T_{\text{map} \to \text{odom}}$, keeping $T_{\text{odom} \to \text{base\_link}}$ smooth and preventing motion control instabilities.

---

## 4. Simulation, SLAM, and Autonomous Navigation Ecosystem

Simulation-based practicals allow students to test algorithms safely before deploying to real physical hardware.

```
+-------------------------------------------------------------------+
|                        RViz2 (Visualization)                      |
+-------------------------------------------------------------------+
                                  ^
                                  | Displays map, costmaps, paths
+-------------------------------------------------------------------+
|                     Nav2 (Navigation Stack)                       |
|   - Global Planner (A* / Dijkstra)                                |
|   - Local Controller (Trajectory Generation)                      |
|   - AMCL (Particle Filter Localization)                           |
+-------------------------------------------------------------------+
           ^                                         |
           | Subscribes /scan, /tf                   | Publishes /cmd_vel
+------------------------------------+               v
|    SLAM Toolbox (Pose-Graph SLAM)  |     +--------------------+
+------------------------------------+     |  Gazebo Simulator  |
           ^                               |  - Robot Kinematics|
           | Subscribes /scan, /odom       |  - Physics Engine  |
           +-------------------------------|  - Sensor Plugins  |
                                           +--------------------+

```

### Core Stack Components

| Software Component | Category | Primary Published Data | Primary Subscribed Data | Primary Function |
| --- | --- | --- | --- | --- |
| **Gazebo Simulator** | Simulation Engine | `/scan`, `/imu`, `odom -> base_link` transform | `/cmd_vel` | Simulates physical dynamics, wheel kinematics, and environmental sensors.

 |
| **`robot_state_publisher`** | Frame Kinematics Engine | Kinematic tree transforms (`/tf`, `/tf_static`) | `/joint_states`, URDF model definitions | Parses URDF/Xacro files to continuously update the spatial frame tree.

 |
| **`slam_toolbox`** | Pose Graph SLAM | 2D Occupancy Grid (`/map`), `map -> odom` transform | Laser scans (`/scan`), `odom -> base_link` transform | Builds 2D grid maps while executing continuous graph pose updates.

 |
| **`nav2_amcl`** | Probabilistic Localization | Particle cloud, `map -> odom` transform | `/scan`, `/map`, `odom -> base_link` transform | Localizes the robot within a pre-built static map using particle filtering.

 |
| **`nav2_bt_navigator`** | Autonomous Behavior Engine | `/navigate_to_pose` (Action interface) | Action Goal specifications | Executes navigation tasks using customizable Behavior Trees.

 |
| **`rviz2`** | Visualization Interface | Interactive goal poses | Visual markers, maps, laser scans, transforms | 3D visual workspace for inspecting spatial transforms and planning trajectories.

 |

---

## 5. Introductory Teaching Notes for Students and Instructors

### The Restaurant Kitchen Analogy

To help beginners quickly grasp ROS 2 communication concepts, use the **Restaurant Kitchen** model:

* **Nodes = Kitchen Staff**: Individual specialists (Chefs, Waiters, Inventory Managers) performing targeted roles.


* **Topics = Kitchen Order Printer / Notice Board**: Waiters post orders asynchronously; any chef can read the incoming orders.


* **Services = Direct Questions**: A chef asking the inventory manager directly if an ingredient is available and waiting for an immediate answer.


* **Actions = Long-Running Tasks**: A customer placing a complex dish order. The chef accepts the goal, periodically reports progress status ("50% ready"), and delivers the final meal, while remaining open to cancellations.



### Workspace Lifecycle & Development Workflow

Students must compile code within structured workspaces using the `colcon` build tool:

1. **Workspace Setup**: Create a workspace directory containing a source folder: `mkdir -p ~/ros2_ws/src`.


2. **Build Process**: Run `colcon build` from `~/ros2_ws/`. This generates three folders:
* `build/`: Holds intermediate build artifacts.


* `install/`: Contains executable binaries and setup configuration files.


* `log/`: Contains compilation logs.




3. **Environment Sourcing**: Register compiled packages into the terminal session by sourcing: `source install/setup.bash`.



### Common Pitfalls in Practical Sessions

1. **Simulation Time Mismatch (`use_sim_time`)**: When running against Gazebo, nodes must process time published on the `/clock` topic rather than host computer clock time. Always pass `use_sim_time:=True` to tools like RViz2 and Nav2 to avoid spatial lookup failures.


2. **Multi-Student Network Cross-Talk (`ROS_DOMAIN_ID`)**: ROS 2 auto-discovers nodes on the local network. If multiple student machines share a local subnet with default settings (`ROS_DOMAIN_ID=0`), cross-talk will occur. Assign a unique integer domain ID to each student workstation: `export ROS_DOMAIN_ID=15`.


3. **Transform Tree Loops**: Connecting `map` directly to `base_link` bypasses `odom` and breaks the single-parent tree rule. Reinforce REP 105 frame chains early.



---

## 6. Suggested Practical Syllabus for University Practicals

| Module # | Topic | Key Theoretical Concepts | Practical Lab Exercise | Diagnostic CLI Tools |
| --- | --- | --- | --- | --- |
| **Module 1** | **ROS 2 Middleware Basics** | DDS architecture, nodes, topic pub/sub, package structures.

 | Building a `colcon` workspace; writing C++/Python publisher and subscriber nodes.

 | `ros2 node list`<br>

<br>`ros2 topic echo`<br>

<br>`ros2 topic hz`<br> |
| **Module 2** | **Services, Actions & Params** | Request/response cycles, action state feedback, runtime configuration.

 | Implementing an Action Server to execute multi-step differential motor rotations.

 | `ros2 service call`<br>

<br>`ros2 action send_goal`<br>

<br>`ros2 param set`<br> |
| **Module 3** | **Transforms & URDF Models** | Kinematic chains, REP 103/105 conventions, `tf2` trees, Xacro modeling.

 | Building a 3D differential-drive URDF robot model; publishing spatial transforms.

 | `ros2 run tf2_tools view_frames`<br>

<br>`ros2 run tf2_ros tf2_echo`<br> |
| **Module 4** | **Physics Simulation** | Sensor simulation plugins, wheel friction, odometric noise and integration drift.

 | Spawning a TurtleBot3 robot inside a Gazebo world; controlling velocity via keyboard teleoperation.

 | `ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py`<br> |
| **Module 5** | **Mapping & 2D Graph SLAM** | Occupancy grid representations, scan matching, loop closure, pose graphs.

 | Driving a simulated mobile platform to map an unknown Gazebo world.

 | `ros2 launch slam_toolbox online_async_launch.py`<br>

<br>`ros2 run nav2_map_server map_saver_cli`<br> |
| **Module 6** | **Localization & Navigation** | Monte Carlo Localization (AMCL), global path planners (A*), local obstacle avoidance.

 | Launching Nav2 to execute autonomous navigation goals to specified poses in RViz2.

 | `ros2 launch nav2_bringup bringup_launch.py`<br> |

---

## 7. Curated Markdown Resources for Course Integration

| Resource Category | Name | Link | Description & Utility |
| --- | --- | --- | --- |
| **Official Documentation** | ROS 2 Documentation (Humble) | [https://docs.ros.org/en/humble/](https://docs.ros.org/en/humble/)<br> | Official API references, core concept tutorials, and CLI command documentation.

 |
| **Official Documentation** | Nav2 Navigation Documentation | [https://docs.nav2.org/](https://docs.nav2.org/)<br> | Architectural breakdowns, behavior tree implementations, and configuration tutorials.

 |
| **System Specifications** | REP 105: Coordinate Frames | [https://www.ros.org/reps/rep-0105.html](https://www.ros.org/reps/rep-0105.html)<br> | Naming conventions and semantic definitions for `earth`, `map`, `odom`, and `base_link`.

 |
| **System Specifications** | REP 103: Units and Axis Conventions | [https://www.ros.org/reps/rep-0103.html](https://www.ros.org/reps/rep-0103.html)<br> | Standards for coordinate axes orientations, rotational signs, and SI measurement units.

 |
| **Code Repositories** | SLAM Toolbox Repository | [https://github.com/SteveMacenski/slam_toolbox](https://github.com/SteveMacenski/slam_toolbox)<br> | Production-grade 2D pose graph mapping stack source code and example configs.

 |
| **Code Repositories** | TurtleBot3 Simulation Packages | [https://github.com/ROBOTIS-GIT/turtlebot3_simulations](https://github.com/ROBOTIS-GIT/turtlebot3_simulations)<br> | Standardized simulation models and Gazebo worlds widely used in university practicals.

 |
| **Educational Repositories** | Autonomous Maze Solving TurtleBot3 | [https://github.com/Preetamk97/Autonomous-Maze-Solving-Turtlebot3-Simulation](https://github.com/Preetamk97/Autonomous-Maze-Solving-Turtlebot3-Simulation)<br> | Complete `ament_cmake` demonstration package featuring Gazebo simulation, SLAM, and Nav2 path planning.

 |
| **Educational Repositories** | MOGI Cognitive Robotics Course | [https://github.com/MOGI-ROS/Week-1-8-Cognitive-robotics](https://github.com/MOGI-ROS/Week-1-8-Cognitive-robotics)<br> | Open-source university course curriculum covering ROS 2 setup, simulation, teleoperation, and navigation.

 |



