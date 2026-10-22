# SLAM Algorithms Explained Simply

Every SLAM algorithm relies on the exact same core blueprint: guessing movement (**Dead Reckoner**), spotting clues in the environment (**Landmark Recogniser**), and updating a room drawing (**Map Builder**). 

The different SLAM algorithms simply change how those three core roles perform their jobs.

---

## 1. Feature-Based SLAM (The Single Master List)

* **Analogy:** Putting push-pins on a blank board for every distinct item seen.
* **Dead Reckoner:** Counts wheel turns to estimate how far the robot rolled forward.
* **Landmark Recogniser:** Looks specifically for sharp, distinct pinpoint features (like a table leg, a door corner, or a unique sign).
* **Map Builder:** Keeps **one single master map**. Every time the landmark recognizer spots a known item, the map builder nudges both the robot's current position and the positions of all surrounding landmarks to keep everything aligned.

---

## 2. Particle Filter SLAM (The Team of Multiple Guesses)

* **Analogy:** Managing a team of hundreds of hypothetical "clones" (particles), where each clone holds its own separate opinion.
* **Dead Reckoner:** Takes all the clones and pushes them forward, giving each clone a slightly different nudge to account for slippery wheels or bumpy floors.
* **Landmark Recogniser:** Acts as a judge. It compares what the real robot's sensors see with what each clone *thinks* it should see. Clones that guessed right get high scores; bad guesses get discarded.
* **Map Builder:** **Replicated inside every clone.** Each clone draws its own personal map of the room based on its own trajectory. The map attached to the winning clone is treated as the true map.

---

## 3. Graph-Based SLAM (The Connect-the-Dots Rubber Band Puzzle)

* **Analogy:** Collecting a history of snapshots and solving the whole layout at once rather than fixing things step-by-step while driving.
* **Dead Reckoner:** Drops a breadcrumb (a pose snapshot) everywhere the robot goes and draws a line connecting snapshot 1 to snapshot 2, snapshot 2 to snapshot 3, and so on.
* **Landmark Recogniser:** Acts as a memory matcher. When driving around a full loop back to the start, it recognizes that snapshot #100 looks identical to snapshot #1. It attaches a "virtual rubber band" directly connecting snapshot #100 to snapshot #1.
* **Map Builder:** Acts as a puzzle solver. It takes all the breadcrumbs and stretchy rubber bands, pulls on them, and lets them snap into place so that all the snapshots line up into one clean room blueprint.

---

## 4. Grid-Based SLAM (The Graph Paper Coloring)

* **Analogy:** Treating the world like a sheet of graph paper rather than looking for specific objects like chairs or doors.
* **Dead Reckoner:** Tracks roughly which square of the graph paper the robot has moved to.
* **Landmark Recogniser:** Doesn't look for unique landmarks. Instead, it takes entire laser distance scans and slides them around over existing wall outlines to find the best overlap.
* **Map Builder:** Fills in the graph paper grid cell by cell. If a laser beam passes straight through a square, the map builder colors it white (empty space). If the laser beam bounces off something, the map builder colors that square dark gray or black (a wall or obstacle).

---

## Summary Comparison Matrix

| SLAM Variation | Landmark Recogniser Role | Map Builder Role | Dead Reckoner Role |
| :--- | :--- | :--- | :--- |
| **Feature-Based** | Spots specific points (table legs, corners) | Nudges 1 master map of points | Moves 1 robot pose estimate |
| **Particle Filter** | Scores which robot guess matches reality | Keeps 1 mini-map per robot guess | Moves hundreds of robot guesses |
| **Graph-Based** | Finds loop closures (re-recognized places) | Solves a rubber-band network of snapshots | Connects sequential pose snapshots |
| **Grid-Based** | Matches entire laser scan shapes | Colors graph paper squares (wall / open space) | Tracks square-by-square grid movement |