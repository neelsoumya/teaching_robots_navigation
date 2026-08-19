# Introduction to Robotics


- path planning
- where you are now?
- `self localisation`: establish own position with respect to a frame of reference

- `controller`
- generate left velocity and right velocity and from that the angle of the robot

- PID Proportional Integrative Derivative controller
- does that remind you of anything? a machine learning algorithm?

- path planning: strategic / long-term
- obstacle avoidance: short term goals

- reinforcememt learning for controller: positive reinforcement


- `Occupancy map`

-  artificial potential field

- grid based techniques

- sample based planning


## Activity

- Read the article on [autonomous mining robots](https://www.bbc.co.uk/news/articles/cgej7gzg8l0o)

- [Lecture on Rio Tinto](riotinto.md)

- how are obstacles detected?

- fixed roads

- base station has map and each vehicle has GPS

-  what is this `virtual bubble`?

-  artificial potential field

- GPS denied (see notes on GPS)

- if you put a new obstacle, then map regenerated and potential field

- disadvantages?

-   




## Learning Objectives

After this chapter you should understand

- What a robot is
- The difference between perception, planning and control
- The robotics software stack
- Why localisation is difficult
- Why SLAM exists

---

## What is a Robot?

A robot is an embodied intelligent system capable of

- sensing its environment
- reasoning about it
- acting upon it

Unlike traditional software, robots interact with the physical world.

Examples include

- warehouse robots
- drones
- self-driving cars
- autonomous submarines
- planetary rovers
- robot vacuum cleaners

---

## The Robotics Pipeline

```
Sensors
   ↓
Perception
   ↓
Localisation
   ↓
Mapping
   ↓
Planning
   ↓
Control
   ↓
Motors
```

---

## Core Problems

### Perception

What is around me?

### Localisation

Where am I?

### Mapping

What does the world look like?

### Planning

Where should I go?

### Control

How do I move there?

---

## Why Robotics is Hard

Unlike software,

- sensors are noisy
- actuators slip
- wheels skid
- GPS disappears
- cameras fail in darkness

Robotics is about making good decisions with imperfect information.

---

## Modern Robotics Stack

Typical sensors

- Camera
- Stereo Camera
- RGB-D Camera
- LiDAR
- IMU
- GPS
- Wheel Encoders
- Radar

Typical algorithms

- EKF
- Particle Filter
- Graph SLAM
- ORB-SLAM
- Cartographer
- RTAB-Map

---

## Reading

Probabilistic Robotics
Thrun, Burgard & Fox

Modern Robotics
Kevin Lynch

Robotics, Vision and Control
Peter Corke
