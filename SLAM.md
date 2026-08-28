# SLAM and other algorithms

## Occupancy map

- exploration of environment

- position estimation using robot pose

- sensor values interpret (LIDAR, sonar, vision, etc.)

- integration of sensor values into map (based on distance from robot and pose estimation of robot)


## SLAM

- Simultaneous Localization and Mapping (SLAM)

- which came first: the egg or the chicken?

- robot wants to go from point A to point B: but it does not know what the world looks like?

- so it needs a map

- but what if there is no map?

- try to build a map when there is no map!

![image](images/slam.png)

- simultaneously map and simultaneously localize

## Workflow

![image](images/workflow.png)


- wheels -> odometry

- if humanoid robot then joints

- IMU inertial measurement unit

- odometry: key to robotics platforms

- odometry assumption: robot should know where is origin (0,0,0)

- for vacuum cleaner, it is charging point. can self localize from there

- all sensor input goes to build occupancy map

- 🤔 ❓ what is the problem?

- relying too much on odomtery

- can be slippage, etc

- self localizing due to odometry can be problematic

- every rotation adds up

- map can be erroneous

- dead reckoning (early days of flight)

- `v = d/t` has a clock, how much distance travelled in a time period

- look for a particular direction on compass

- and then look for a landmark

- _LondonEye_ is a landmark for flights

- correct for drift

- greater the distance between landmarks, the greater the drift

- can miss landmark

![image](images/dead_reckoning.png)

- static 

- vacuum robot : not move chairs

- distinct landmarks and unique locations (QR codes, colours)

- database of landmarks with locations

- weights landmark more than odometry and then update location

- equations

![image](images/dead_equations.png)

- 🤔 ❓ imagine you have been asked to design a vacuum robot that will work in an office with glass doors. what problems will you face?

- problem with _laser_: can shine through, narrow beam


- glass may refract

- with glass room, use _ultrasound_

- design issues in industry: vacuum robot in glass offices, but office may have glass

- combinations of sensors

- landmarks may look similar

- building a robotic tour guide (in _Legoland_)

- landmarks locations known and do not move

![image](images/slam_pose.png)

- waypoint navigation using landmarks

![image](images/waypoint.png)

## Rvis

- Rvis will show lasers as dots

## Particle Filters

- particles generated

- Initialization: The robot starts with no prior knowledge, so it scatters potential positions (particles) uniformly across the map.

- Prediction: As the robot moves, it uses its motion model, combined with added random noise to account for uncertainty, to propagate all particles.

- Correction: The robot takes sensor measurements (e.g., via Lidar). Each particle predicts what it would measure. Particles whose predictions closely match the actual measurements are given a high "importance weight."

- Resampling: A new set of particles is formed, favoring those with high weights. This effectively eliminates unlikely hypotheses and duplicates the most plausible ones

- Convergence: The process repeats, and over multiple cycles, the cloud of particles converges on the robot's actual pose.

![image](images/particlefilters.png)

- constantly resample and refine positions

- 🤔 ❓do you have a particle filter in your brain?


 
