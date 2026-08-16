# Evaluation

- How to evaluate your systems (robots, UAVs)?

- [PDF](evals.pdf)

- [Evaluation app](sensor_evaluation_app.html)


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


## More resources
# **Teaching Module: Sensor Evaluation & Engineering Trade-Offs in Robotics and UAVs**

**Course:** Advanced Mobile Robotics / Unmanned Aerial Systems (UAVs)

**Target Audience:** Undergraduate / Master's Level Engineering Students

**Topic:** Empirical Sensor Evaluation, Failure Modes, Power/Weight Trade-offs, and System Integration

## **1\. Executive Summary & Pedagogical Goals**

When designing autonomous systems, students often assume sensors operate under ideal mathematical assumptions. In practice, sensor selection is driven by physical environment noise, payload weight limits, and battery constraints.

### **Key Learning Objectives**

1. **Analyze physical sources of sensor inaccuracy** across LiDAR, cameras, and IMUs—with special emphasis on UAV dynamics.  
2. **Evaluate the power-weight-throughput triangle** in aerial vs. ground robotics.  
3. **Formulate concrete sensor fusion strategies** that compensate for individual sensor failure modes without exceeding onboard energy budgets.

## **2\. Sensor Inaccuracies & Failure Modes**

### **A. LiDAR (Light Detection and Ranging)**

LiDAR measures time-of-flight (![][image1]) of emitted laser pulses to compute distance ![][image2].

* **Ground Robotics Failure Modes:**  
  * **Narrow Beam / Target Miss:** A narrow beam (e.g., ![][image3]) hitting a small target at range ![][image4] can easily miss or slip past edges, causing "infinite" distance readings or wall reflections behind the target.  
  * **Specular Reflection & Absorbent Surfaces:** Dark matte materials absorb the beam; glossy/glass surfaces cause specular bounce, directing the return signal away from the receiver.  
* **UAV-Specific Failure Modes:**  
  * **High-Frequency Motor Vibration:** Rotor vibration induces high-frequency angular jitter (![][image5]). At a distance of ![][image6], an angular jitter of ![][image7] creates a positional drift error ![][image8].  
  * **Incidence Angle Deviation:** As a drone tilts (pitches/rolls) to maneuver, the laser beam strikes the ground or targets at oblique angles, spreading the footprint and lowering signal-to-noise ratio.  
  * **Dust, Fog, and Prop Wash Dust:** Propeller wash near the ground kicks up particulates, causing false-positive obstacle detection.

### **B. Visual Sensors & RGB-D Cameras**

* **Ground Robotics Failure Modes:** Lighting variation, motion blur at high angular turning rates, scale ambiguity in monocular setups.  
* **UAV-Specific Failure Modes:**  
  * **Rapid Exposure Changes:** Moving quickly from shaded canopy to bright sunlight causes sensor saturation.  
  * **High-Speed Rolling Shutter Artifacts:** Unmanned aircraft moving at ![][image9] experience image warping when using low-cost rolling shutter CMOS sensors.  
  * **Computational Overhead:** Processing ![][image10] video streams at ![][image11] for optical flow or visual SLAM consumes significant CPU/GPU power.

### **C. Inertial Measurement Units (IMU) & GPS/GNSS**

* **UAV Multi-Pathing & Drift:** GPS signal reflections off buildings (multipathing) lead to sudden ![][image12] position jumps. Relying solely on dead reckoning with an uncalibrated MEMS IMU leads to quadratic error growth over time (![][image13]).

## **3\. Power, Weight, and Energy Constraints**

In ground robotics, adding a ![][image14] sensor suite increases motor draw slightly. In aerial robotics (UAVs), payload mass penalizes flight time non-linearly.

### **The UAV Payload Energy Penalty**

Hover thrust required is directly proportional to total mass ![][image15]:

![][image16]Power required for a multirotor to hover scales according to momentum theory:

![][image17]Adding a ![][image18] mechanical LiDAR package to a ![][image19] drone increases mass by ![][image20], but increases hover power draw by approximately:

![][image21]\+-----------------------------------------------------------------------+  
|                         THE SYSTEM TRADEOFF                           |  
|                                                                       |  
|   \+-------------------+        Higher Weight       \+---------------+  |  
|   |   Heavy Sensor    | \-------------------------\> | Short Flight  |  |  
|   |  (High Precision) |                            |    Duration   |  |  
|   \+-------------------+                            \+---------------+  |  
|             |                                              ^          |  
|             | High Data Rate                               |          |  
|             v                                              |          |  
|   \+-------------------+        High Wattage        \+---------------+  |  
|   | Onboard Compute   | \-------------------------\> | Battery Drain |  |  
|   |  (GPU/Edge AI)    |                            |               |  |  
|   \+-------------------+                            \+---------------+  |  
\+-----------------------------------------------------------------------+

### **Sensor Category Comparison Matrix**

| Sensor Type | Typical Weight | Power Draw | Accuracy Range | Primary Failure Mode | Best Engineering Use Case |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Mechanical LiDAR** | **![][image22]** | **![][image23]** | High (![][image24]) | Vibration, High Power, Mass | High-precision 3D Terrain Mapping |
| **Solid-State LiDAR** | **![][image25]** | **![][image26]** | Medium-High (![][image27]) | Limited Field of View (![][image28]) | UAV Frontal Obstacle Avoidance |
| **Stereo Camera** | **![][image29]** | **![][image30]** | Medium (Degrades with range) | Low light, Featureless walls | Close-range VIO & Landing Alignment |
| **Ultrasonic Rangefinder** | **![][image31]** | **![][image32]** | Low (![][image33]) | Soft surfaces, Angular limits | Low-altitude Ground Proximity Hold |

## **4\. Classroom Case Studies & Practical Exercises**

### **Case Study 1: The Multi-Robot Contaminated Barrel Cleanup (Ground)**

* **Context:** A ground robot must approach, attach to, and transport toxic barrels.  
* **Failure Encountered:** The 1° LiDAR beam misses small target barrels at range ![][image34], returning inf.  
* **Engineering Outcome:** Re-architect system roles. Use the camera (blob detection) for mid-range tracking and estimation, restricting LiDAR to close-range (![][image35]) collision prevention.

### **Case Study 2: Powerline Inspection UAV (Aerial)**

* **Context:** Autonomous drone scanning thin powerlines (![][image36] diameter) at ![][image37] distance.  
* **Failure Encountered:** Solid-state LiDAR FOV misses thin wires when the drone yaws rapidly. Stereo cameras fail due to sun glare.  
* **Engineering Outcome:** Combine a high-frame-rate solid-state LiDAR (![][image38]) with an IMU-driven kalman filter. Enforce a flight speed cap (![][image39]) to bound braking distance within the maximum detection range.

## **5\. Homework & Lab Assignment Ideas**

### **Assignment 1: Sensor Trade-Off Calculations**

**Task:** Given a ![][image40] baseline quadcopter with a ![][image41] battery (![][image42]), calculate total hover time under two payloads:

1. **Option A:** Stereo Camera Suite (![][image43], ![][image44] power draw).  
2. **Option B:** Mechanical 3D LiDAR (![][image45], ![][image46] power draw).

*Students must apply the ![][image47] relationship and account for sensor electrical draw to plot flight time degradation.*

### **Assignment 2: Failure Mode Analysis & FSM Design**

**Task:** Design a state machine (or RoboChart) for an inspection drone encountering sensor degradation.

* **Condition 1:** Camera lens is covered in dust (Image entropy drops below threshold).  
* **Condition 2:** LiDAR returns zero valid points for ![][image48].  
* **Required Student Solution:** System must safely transition to a stable altitude hold using IMU/barometer and initiate a controlled vertical land or return-to-home protocol.

## **6\. Seminar Discussion Prompts**

1. *"Why might a $50 ultra-sonic sensor be a better choice for low-altitude UAV altitude hold than a $1,500 lightweight LiDAR?"*  
   *(Key points: Power draw, mass penalty, low compute needs, reliability over flat non-absorbing surfaces).*  
2. *"If a system's reported sensor accuracy is high in simulation, why does performance often degrade significantly when deployed on real hardware?"*  
   *(Key points: Sensor noise models in simulators are often Gaussian and ignore environmental interference like prop-wash, glare, temperature drift, and dynamic vibration).*




|   +-------------------+        Higher Weight       +---------------+  |

|   |   Heavy Sensor    | -------------------------> | Short Flight  |  |
|   |  (High Precision) |                            |    Duration   |  |
|   +-------------------+                            +---------------+  |
|             |                                              ^          |
|             | High Data Rate                               |          |
|             v                                              |          |
|   +-------------------+        High Wattage        +---------------+  |
|   | Onboard Compute   | -------------------------> | Battery Drain |  |
|   |  (GPU/Edge AI)    |                            |               |  |
|   +-------------------+                            +---------------+  |
+-----------------------------------------------------------------------+
Sensor Category Comparison MatrixSensor TypeTypical WeightPower DrawAccuracy RangePrimary Failure ModeBest Engineering Use CaseMechanical LiDAR$500\text{g} - 1.5\text{kg}$$10\text{W} - 35\text{W}$High ($\pm 1-3\text{ cm}$)Vibration, High Power, MassHigh-precision 3D Terrain MappingSolid-State LiDAR$100\text{g} - 300\text{g}$$2\text{W} - 6\text{W}$Medium-High ($\pm 3-5\text{ cm}$)Limited Field of View ($60^\circ-90^\circ$)UAV Frontal Obstacle AvoidanceStereo Camera$50\text{g} - 150\text{g}$$1.5\text{W} - 3\text{W}$Medium (Degrades with range)Low light, Featureless wallsClose-range VIO & Landing AlignmentUltrasonic Rangefinder$10\text{g} - 30\text{g}$$<0.5\text{W}$Low ($\pm 5-10\text{ cm}$)Soft surfaces, Angular limitsLow-altitude Ground Proximity Hold4. Classroom Case Studies & Practical ExercisesCase Study 1: The Multi-Robot Contaminated Barrel Cleanup (Ground)Context: A ground robot must approach, attach to, and transport toxic barrels.Failure Encountered: The 1° LiDAR beam misses small target barrels at range $> 3\text{ m}$, returning inf.Engineering Outcome: Re-architect system roles. Use the camera (blob detection) for mid-range tracking and estimation, restricting LiDAR to close-range ($< 1\text{ m}$) collision prevention.Case Study 2: Powerline Inspection UAV (Aerial)Context: Autonomous drone scanning thin powerlines ($1-2\text{ cm}$ diameter) at $15\text{ m}$ distance.Failure Encountered: Solid-state LiDAR FOV misses thin wires when the drone yaws rapidly. Stereo cameras fail due to sun glare.Engineering Outcome: Combine a high-frame-rate solid-state LiDAR ($100\text{ Hz}$) with an IMU-driven kalman filter. Enforce a flight speed cap ($v \le 2\text{ m/s}$) to bound braking distance within the maximum detection range.5. Homework & Lab Assignment IdeasAssignment 1: Sensor Trade-Off CalculationsTask: Given a $1.8\text{ kg}$ baseline quadcopter with a $4\text{S } 5000\text{ mAh}$ battery ($74\text{ Wh}$), calculate total hover time under two payloads:Option A: Stereo Camera Suite ($120\text{ g}$, $2.5\text{ W}$ power draw).Option B: Mechanical 3D LiDAR ($850\text{ g}$, $18\text{ W}$ power draw).Students must apply the $P \propto m^{1.5}$ relationship and account for sensor electrical draw to plot flight time degradation.Assignment 2: Failure Mode Analysis & FSM DesignTask: Design a state machine (or RoboChart) for an inspection drone encountering sensor degradation.Condition 1: Camera lens is covered in dust (Image entropy drops below threshold).Condition 2: LiDAR returns zero valid points for $> 500\text{ ms}$.Required Student Solution: System must safely transition to a stable altitude hold using IMU/barometer and initiate a controlled vertical land or return-to-home protocol.6. Seminar Discussion Prompts"Why might a $50 ultra-sonic sensor be a better choice for low-altitude UAV altitude hold than a $1,500 lightweight LiDAR?"(Key points: Power draw, mass penalty, low compute needs, reliability over flat non-absorbing surfaces)."If a system's reported sensor accuracy is high in simulation, why does performance often degrade significantly when deployed on real hardware?"(Key points: Sensor noise models in simulators are often Gaussian and ignore environmental interference like prop-wash, glare, temperature drift, and dynamic vibration).


