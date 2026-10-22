# SLAM Algorithm Variations: Technical Verification & Architectural Mapping

This document provides a detailed breakdown of how major SLAM paradigms (EKF-SLAM, FastSLAM, Graph-SLAM, and Grid-based SLAM) map onto the core navigation architecture centered around the **Landmark Recogniser**, **Dead Reckoner**, and **Map Builder**.

---

## 1. Architectural Foundation

All standard SLAM variations share a unified functional decomposition:
* **Inputs / Hardware Layer:** Exteroceptive sensors (LiDAR, Cameras) and Proprioceptive sensors (Encoders, IMUs).
* **The Core Triad:**
  1. **Landmark Recogniser (Frontend Perception):** Transforms raw sensor data into observation updates, feature associations, or geometric constraints.
  2. **Dead Reckoner (Motion Estimation):** Propagates motion estimates and tracks uncertainty accumulated over time.
  3. **Map Builder (Backend Estimation Engine):** Fuses motion estimates and observations to compute the joint spatial estimate of the robot trajectory and environment map.

---

## 2. Technical Analysis of the 4 Variations

### Variation 1: Feature-Based SLAM (Extended Kalman Filter - EKF SLAM)

#### Overview
EKF-SLAM represents the classic parametric approach where the environment is modeled as a set of sparse geometric landmarks, and uncertainty is modeled strictly as a Gaussian distribution.

#### Mathematical Formulation
The state vector $\mathbf{x}_t$ concatenates the 2D/3D robot pose $\mathbf{x}_r$ with the positions of $N$ static landmarks $\mathbf{m}_1, \dots, \mathbf{m}_N$:

$$\mathbf{x}_t = \begin{bmatrix} \mathbf{x}_r \\ \mathbf{m}_1 \\ \vdots \\ \mathbf{m}_N \end{bmatrix}_{((3+2N) \times 1)}, \quad \mathbf{\Sigma}_t = \begin{bmatrix} \mathbf{\Sigma}_{rr} & \mathbf{\Sigma}_{rm} \\ \mathbf{\Sigma}_{mr} & \mathbf{\Sigma}_{mm} \end{bmatrix}$$

#### Mapping to Architecture Modules
* **Dead Reckoner (Prediction Step):**
  Uses the kinematic motion model $g(\mathbf{x}_{r, t-1}, u_t)$ to predict the mean robot pose $\bar{\mathbf{x}}_{r, t}$ and updates robot pose covariance $\bar{\mathbf{\Sigma}}_{rr, t}$.
* **Landmark Recogniser (Data Association):**
  Extracts discrete geometric point/line features from sensors and computes predicted observations $\hat{\mathbf{z}}_i = h(\bar{\mathbf{x}}_{r, t}, \mathbf{m}_{i})$. Calculates innovation:

  $$\mathbf{y}_i = \mathbf{z}_i - \hat{\mathbf{z}}_i$$

* **Map Builder (Correction Step):**
  Computes the Kalman Gain $K_t = \bar{\mathbf{\Sigma}}_t H_t^T (H_t \bar{\mathbf{\Sigma}}_t H_t^T + R_t)^{-1}$ to update the entire joint state vector $\mathbf{x}_t$ and full covariance matrix $\mathbf{\Sigma}_t$.

#### Teaching Key takeaway
* **Complexity:** $\mathcal{O}(N^2)$ update cost due to maintaining dense off-diagonal covariance entries ($\mathbf{\Sigma}_{rm}$).
* **Limitation:** Cannot recover from incorrect data associations; susceptible to linearization errors in non-linear measurement models.

---

### Variation 2: Particle Filter SLAM (FastSLAM / RBPF)

#### Overview
FastSLAM uses Rao-Blackwellized Particle Filtering (RBPF) to solve the multi-modal distribution problem and scale beyond the $O(N^2)$ limitation of EKF-SLAM.

#### Mathematical Factorization
Exploits conditional independence: given the true robot trajectory $x_{1:t}$, landmark locations $m_1, \dots, m_N$ are conditionally independent of one another:

$$P(x_{1:t}, M \mid z_{1:t}, u_{1:t}) = P(x_{1:t} \mid z_{1:t}, u_{1:t}) \prod_{i=1}^{N} P(m_i \mid x_{1:t}, z_{1:t})$$

#### Mapping to Architecture Modules
* **Dead Reckoner (Proposal Distribution):**
  Each particle $k \in \{1, \dots, K\}$ samples a new robot pose independently from the probabilistic motion model:

  $$x_t^{(k)} \sim P(x_t \mid x_{t-1}^{(k)}, u_t)$$

* **Landmark Recogniser (Weighting Step):**
  Evaluates observation likelihood to compute the importance weight $w^{(k)}$ for each particle based on how closely predicted observations match actual measurements.
* **Map Builder (Replicated per Particle):**
  Instead of one global covariance matrix, each particle contains its own trajectory history and $N$ individual $2 \times 2$ EKFs—one per landmark.

#### Teaching Key Takeaway
* **Complexity:** Reduces complexity to $\mathcal{O}(K \log N)$, where $K$ is the number of particles.
* **Limitation:** Particle depletion in large environments requiring frequent resampling.

---

### Variation 3: Graph-Based SLAM (Pose Graph / Factor Graph)

#### Overview
Modern industry-standard SLAM framing (e.g., ORB-SLAM, Cartographer, GTSAM). Replaces recursive filtering with non-linear global optimization over a graph network.

#### Mathematical Formulation
Constructs a graph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$ where vertices $\mathcal{V}$ are robot poses $x_i$ and edges $\mathcal{E}$ are spatial constraints $z_{ij}$. Solves the non-linear least-squares problem:

$$\mathbf{x}^* = \arg\min_{\mathbf{x}} \sum_{(i,j) \in \mathcal{E}} \mathbf{e}_{ij}(\mathbf{x}_i, \mathbf{x}_j)^T \mathbf{\Omega}_{ij} \mathbf{e}_{ij}(\mathbf{x}_i, \mathbf{x}_j)$$

where $\mathbf{e}_{ij}$ is the error residual between predicted and measured relative transforms, and $\mathbf{\Omega}_{ij}$ is the information matrix.

#### Mapping to Architecture Modules
* **Dead Reckoner (Odometry Edges):**
  Computes frame-to-frame odometry transformations (via wheel encoders, IMU pre-integration, or visual odometry) to create sequential graph edges $z_{t-1, t}$.
* **Landmark Recogniser (Loop Closure Edges):**
  Performs place recognition (e.g., Bag-of-Words / DBoW2). When a previously visited place is recognized, it creates non-sequential loop closure edges $z_{i, j}$.
* **Map Builder (Graph Optimization Engine):**
  Executes iterative sparse matrix solvers (Gauss-Newton, Levenberg-Marquardt) using libraries like `g2o` or `GTSAM` to adjust the full pose sequence simultaneously.

#### Teaching Key Takeaway
* **Advantage:** Highly scalable due to matrix sparsity; decouples perception frontend from optimization backend.

---

### Variation 4: Grid-Based SLAM (GMapping / Occupancy Grid SLAM)

#### Overview
Used extensively in indoor ground robotics where spatial boundaries (walls, obstacles) cannot be easily parameterized by discrete geometric primitives (points/lines).

#### Mathematical Formulation
Discretizes space into a grid of cells $m_i \in \{0, 1\}$ (free/occupied). Updates each cell independently using log-odds representation $l_t(m_i)$:

$$l_t(m_i) = l_{t-1}(m_i) + \text{inv\_sensor\_model}(z_t, x_t) - l_0$$

where $l_0 = \log \frac{P(m_i=1)}{P(m_i=0)}$ is the prior.

#### Mapping to Architecture Modules
* **Dead Reckoner:** Provides motion prediction used as an initial seed for scan matching.
* **Landmark Recogniser (Scan Matcher):**
  Instead of identifying discrete landmarks, matches dense LiDAR scan point clouds directly against existing submaps (e.g., via ICP or Correlative Scan Matching).
* **Map Builder (Occupancy Update Engine):**
  Performs raycasting (e.g., Bresenham's algorithm) along sensor beams to update free and occupied log-odds probabilities across grid cells.

---

## 3. Comparative Matrix

| Paradigm | Landmark Recogniser Role | Dead Reckoner Role | Map Builder Backend | Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **EKF-SLAM** | Geometric feature extractor (corners/lines) | Kinematic state prediction | Single joint covariance update ($\mathbf{\Sigma}_t$) | $\mathcal{O}(N^2)$ |
| **FastSLAM** | Feature matcher for likelihood evaluation | Particle motion sampling | $K$ independent sets of landmark EKFs | $\mathcal{O}(K \log N)$ |
| **Graph-SLAM** | Scan matching & Loop closure detector | Odometry constraint generator ($\mathbf{z}_{i, j}$) | Sparse Non-linear Least-Squares ($\mathbf{g2o}/\mathbf{GTSAM}$) | $\mathcal{O}(|\mathcal{V}| + |\mathcal{E}|)$ |
| **Grid-SLAM** | Dense scan-to-map alignment (ICP) | Odometry prior calculation | Raycasting & Log-odds grid updates | $\mathcal{O}(\text{Grid Cells})$ |

---

## 4. Graphic Errata & Presentation Notes

When presenting the generated synthesis diagram in class, note the following rendering corrections for student clarity:

1. **Variation 2 Box (Top Right):**
   * *Graphic text:* `"Core core replicatom particles:"`
   * *Correction:* **"Core modules replicated per particle"**
2. **Central Architecture Box (Bottom Center):**
   * *Graphic text:* `WHEEL ENCODER (or suimetry)`
   * *Correction:* **"WHEEL ENCODER (or similar for odometry)"**
3. **Variation 3 Box (Bottom Left):**
   * *Graphic text:* `Incremental Pose Contstraints`
   * *Correction:* **"Incremental Pose Constraints"**