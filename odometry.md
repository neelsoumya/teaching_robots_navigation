# Odometry

Odometry is the use of motion sensor data (such as wheel encoders or IMUs) to estimate how an object’s position and orientation change over time, usually relative to a starting point.[1][5][8]

## Basic idea

Odometry works by measuring small increments of motion (for example, wheel rotations) and mathematically integrating them to update an estimate of position and heading step by step.[1][2][5] Because it uses only onboard sensors, it is popular for robots and vehicles to track their pose when GPS or external references are unavailable.[3][6][7]

In practice, a robot starts from a known pose (position and heading) and repeatedly adds small changes computed from its motion sensors.[2][5] Over time, this produces a continuous estimate of where the robot is and how it is oriented in its environment.[1][3]

## Typical sensors

Common odometry setups use wheel encoders on mobile robots or vehicles to measure how far each wheel has turned.[1][2][5] These encoder readings are converted into linear and rotational motion of the robot based on its geometry (wheel radius, track width, number of wheels, and configuration).[2][10]

Many systems combine wheel encoders with inertial measurement units (IMUs), which include accelerometers and gyroscopes, to get better estimates of rotation and short‑term motion.[6][8] More advanced approaches use cameras (visual odometry) or LiDAR to infer motion by tracking changes in the observed environment between successive frames.[6][7][8]

## Main uses

Odometry is a core technique for localization, meaning estimating where a robot or device is relative to a starting point or a known coordinate frame.[5][6][7] It is widely used in mobile robots, autonomous vehicles, and indoor navigation systems for tasks like path following, mapping, and autonomous routines.[1][3][4][5]

In robotics competitions and practical robots, odometry provides live position data to planning and control code so that the robot can follow trajectories, align with field elements, or return to known locations.[4][10] Frameworks like ROS represent odometry information in standardized message formats (such as `nav_msgs/Odometry`) that include estimated pose and velocity in a specific coordinate frame.[9]

## Limitations and drift

Odometry repeatedly integrates small motion measurements, so any sensor error, wheel slip, or incorrect model of the robot’s geometry accumulates over time.[1][2][3][6] This accumulation produces drift, where the estimated position gradually diverges from the true position, especially over long distances or on slippery or uneven terrain.[1][3][8]

Because of this drift, odometry is rarely used alone for long‑term accurate navigation.[2][6][7] Practical systems often fuse odometry with other sources such as GPS, cameras (visual odometry), LiDAR, or map‑based localization to correct errors and keep the pose estimate aligned with reality.[2][6][7][8]

## Visual odometry

Visual odometry uses images from one or more cameras to estimate the position and orientation of a device over time by analyzing how visual features move from frame to frame.[6][7] Instead of relying on wheel rotations, visual odometry tracks points or patterns in the environment, computes their motion, and infers the camera’s motion that would explain these changes.[6][7]

Visual odometry is especially useful for systems where wheel sensors are unavailable or unreliable, such as drones, handheld devices, or robots on soft or slippery surfaces.[6][7] It is often combined with inertial sensors (visual‑inertial odometry) and map‑building techniques to improve robustness and accuracy.[6][7]

## Odometry vs localization

Odometry is one specific technique within the broader task of localization.[5][8] Localization refers to estimating a robot’s pose using any available information, such as odometry, maps, external beacons, GPS, or sensor matching to known landmarks.[5][8]

Odometry typically provides fast, continuous, and local pose updates but drifts over time, while global localization methods periodically correct this drift using more stable references.[2][6][7] Many modern navigation systems run odometry and global localization together to combine responsiveness with long‑term accuracy.[2][6][7][8]
