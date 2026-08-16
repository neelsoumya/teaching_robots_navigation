# Evaluation

- How to evaluate your systems (robots, UAVs)?

## Example of LIDAR

LiDAR works like "laser radar"—it fires invisible light beams and measures how long they take to bounce back to calculate precise distances. Here is how the LiDAR was evaluated in this ground robot report, along with how that same process translates to flying drones (UAVs).

**Ground Robot LiDAR Evaluation (This Project)**

* **The Problem Discovered**: The LiDAR's laser beam was extremely narrow ($1^\circ$ wide). When aiming at a 30 cm barrel from 3 meters away, even a tiny aiming error caused the laser to miss the barrel, hit the back wall, and report that nothing was there (returning an "infinite" distance).


* **The Test Method**: The author ran 12 controlled tests comparing the laser readings against camera images. By measuring how large the barrel appeared in the camera image (its "blob area"), they proved mathematically that camera size was far more reliable for calculating distance than the narrow laser.


* **The Practical Outcome**: The evaluation proved that LiDAR could not be trusted to discover distant barrels. As a result, the camera was assigned to estimate distances, while the LiDAR was restricted to acting as a close-range safety bumper during the final 1 meter of movement.



**LiDAR Evaluation for UAVs (Drones)**

In aerial robotics, LiDAR isn't just looking at barrels—it is mapping terrain, avoiding power lines, or holding altitude. Evaluating a UAV's LiDAR focuses on four different real-world challenges:

* **Vibration & Jitter**: Drone motors vibrate heavily in mid-air. Evaluation tests whether prop-shake distorts the laser beam or creates phantom obstacles in the drone's flight path.
* **Surface Reflection & Angles**: Drones shoot lasers downward at steep, shifting angles. Testing checks if the laser signal gets lost or scattered when hitting reflective or absorbent surfaces like water, windshields, or wet asphalt.
* **Max Altitude Limits**: Unlike a ground robot constrained by walls, a drone moves in three dimensions. Testing establishes the maximum flying height at which the laser can hit the ground and bounce back with a readable signal.
* **Payload & Power Constraints**: UAVs have strict weight and battery limits. Evaluation measures whether the LiDAR's range and scanning speed justify its battery drain and extra payload weight.


