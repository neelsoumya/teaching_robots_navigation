# Introduction to Robotics

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
