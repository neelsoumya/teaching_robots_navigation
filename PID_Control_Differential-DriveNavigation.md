# PID Control for Differential-Drive Robot Navigation

Teaching notes: robot geometry, the meaning of v and ω, the wheel equations, and the PID law that produces ω.

## 1. The robot and its state

The robot's pose is three numbers:

**q = (x, y, θ)**

- (x, y) is the position of the robot's centre, midway between the two wheels, in the world frame.
- θ is the heading, the angle of the robot's forward direction measured counter-clockwise from the world x-axis, in radians.
- L is the wheelbase (track width): the distance between the two wheel contact points. The wheels sit at ±L/2 from the centre.

A differential-drive robot has only two independent actuators, the left and right wheels. It cannot slide sideways, which is the non-holonomic constraint.

## 2. What v and ω mean

Instead of commanding wheels directly, the controller commands two body-level quantities:

- **v** (m/s) is the **linear velocity**, how fast the robot centre moves along its forward direction.
- **ω** (rad/s) is the **angular velocity** (yaw rate), how fast the heading changes: ω = dθ/dt. **Positive ω is a counter-clockwise (left) turn**, which is the ROS convention.

The robot's motion in the world follows from these:

- dx/dt = v cos θ
- dy/dt = v sin θ
- dθ/dt = ω

In code, with timestep Δt:

- x(k+1) = x(k) + v cos θ(k) · Δt
- y(k+1) = y(k) + v sin θ(k) · Δt
- θ(k+1) = θ(k) + ω · Δt

A good place to stress: v moves the robot along its heading and ω only rotates that heading. Steering is indirect, which is why a controller is needed.

## 3. Deriving the wheel equations (the "Wheel calculation" box)

Treat the robot as a rigid body rotating about its centre with angular velocity ω while the centre translates at v. Any point on a rigid body has velocity

**v\_point = v\_centre + ω × r**

where r is the point's offset from the centre. Use body axes: x\_b forward, y\_b to the left. Then:

- the left wheel is at r\_L = (0, +L/2)
- the right wheel is at r\_R = (0, −L/2)
- the angular velocity vector is (0, 0, ω)

The cross product ω × r for r = (0, r\_y) gives (−ω r\_y, 0) in body coordinates. So the forward speed of each wheel is:

**v\_L = v − ω L / 2**

**v\_R = v + ω L / 2**

These are the equations in the diagram. A sanity check for students: for a left turn, ω > 0, so v\_R > v\_L. The outer wheel (right) spins faster, which is exactly what happens when you turn left.

**Inverse relations** (useful for odometry, which goes from wheels back to the body):

- v = (v\_R + v\_L) / 2
- ω = (v\_R − v\_L) / L

So v is the average of the two wheel speeds and ω is their difference divided by L.

**Special cases:**

| Command | Result |
| --- | --- |
| ω = 0 | v\_L = v\_R = v: straight line |
| v = 0, ω ≠ 0 | v\_L = −v\_R: spin on the spot |
| v\_L = 0 | Pivot about the left wheel |

**Turning radius:** the robot follows a circle of radius R = v / ω (infinite when ω = 0).

**To motor commands:** wheel linear speeds convert to wheel angular speeds with φ̇ = v\_wheel / r\_w, where r\_w is the wheel radius.

## 4. Where PID fits

The path planner gives waypoints (x₁, y₁), (x₂, y₂), …, (xₙ, yₙ). The controller must turn the *current target waypoint* (x\_g, y\_g) into v and ω. A common and teachable design:

- **v** is set simply, either constant or reduced when the heading error is large or the goal is near.
- **ω** is the output of the **PID controller**, steering the heading toward the target.

**Heading error.** First compute the desired heading toward the waypoint:

**θ\_d = atan2(y\_g − y, x\_g − x)**

Then the error:

**e = θ\_d − θ**

**Angle wrapping matters.** Angles live on a circle, so e must be wrapped into (−π, π\]:

**e ← atan2(sin e, cos e)**

Without this, a robot at θ = 179° with target −179° sees an error of −358° and spins nearly all the way round instead of turning 2°. This is the most common student bug.

## 5. The PID law

**ω(t) = K\_p · e(t) + K\_i · ∫ e(τ) dτ + K\_d · de(t)/dt**

**Proportional term (K\_p e).** Turn harder the further off-heading you are. Too small is sluggish. Too large overshoots and oscillates (the robot weaves).

**Integral term (K\_i ∫ e).** It accumulates past error, so it removes persistent bias, such as one motor being slightly weaker, which would otherwise leave a steady offset. Too large causes slow oscillation and windup.

**Derivative term (K\_d de/dt).** It reacts to how fast the error is changing, acting as damping. It anticipates overshoot: if the error is shrinking quickly, it backs off the turn.

**Units** (a nice check for students). The error is in rad and ω in rad/s, so K\_p has units of 1/s, K\_i of 1/s², and K\_d is dimensionless.

**Discrete version** (what you actually code, with Δt the control period):

- I(k) = I(k−1) + e(k) · Δt
- D(k) = (e(k) − e(k−1)) / Δt
- ω(k) = K\_p e(k) + K\_i I(k) + K\_d D(k)

### Why P alone already works (intuition)

The heading obeys dθ/dt = ω. With P-only control and a fixed target, de/dt = −K\_p e, so

**e(t) = e(0) · exp(−K\_p t)**

The error decays exponentially with time constant 1/K\_p. In an ideal world there is no overshoot. Real overshoot comes from motor lag, delays and the moving target, which is exactly why K\_d helps.

## 6. Practical details to teach

1. **Saturation.** Motors have limits ±v\_max, so the computed v\_L, v\_R may exceed them. Clipping each wheel separately *changes the turn radius*. Better to scale both by the same factor to preserve the ratio.
2. **Anti-windup.** If ω is saturated, stop accumulating the integral (clamp I or freeze it), otherwise it overshoots badly after saturation.
3. **Derivative noise.** Differentiating noisy measurements amplifies the noise. Low-pass filter D, or differentiate the measurement rather than the error, which avoids a spike when the waypoint changes.
4. **Waypoint switching.** Advance to the next waypoint when the distance sqrt((x\_g − x)² + (y\_g − y)²) is less than a tolerance ε, otherwise the robot circles a waypoint it can't quite reach.
5. **Slow down when misaligned.** For example v = v\_max · cos(e) for |e| < π/2, otherwise 0. The robot then turns before driving.
6. **Tuning order.** Set K\_i = K\_d = 0 and raise K\_p until it just starts oscillating. Add K\_d to damp it, then add a small K\_i only if there's steady drift.

## 7. Worked example

Take L = 0.5 m, v = 0.4 m/s, K\_p = 1.5 s⁻¹, K\_i = 0, K\_d = 0.2. Suppose the heading error is e = 0.3 rad and it is shrinking at de/dt = −0.1 rad/s.

- ω = 1.5(0.3) + 0.2(−0.1) = 0.45 − 0.02 = **0.43 rad/s**
- v\_L = 0.4 − 0.43 × 0.25 = **0.2925 m/s**
- v\_R = 0.4 + 0.43 × 0.25 = **0.5075 m/s**

Check with the inverse: ω = (0.5075 − 0.2925) / 0.5 = 0.43 ✓, and v = (0.5075 + 0.2925) / 2 = 0.4 ✓. The right wheel is faster, so the robot turns left, which is correct since e > 0.

## 8. Variant worth mentioning

Instead of heading error, you can run PID on **cross-track error** d (the perpendicular distance to the path segment). This suits line following better, and with the same structure, ω = K\_p d + K\_i ∫ d + K\_d dd/dt. Heading-to-waypoint is simpler to teach first.
