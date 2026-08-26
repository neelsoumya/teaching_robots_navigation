# ROS 2 hello world, on a Mac, in VS Code

## What we're building

ROS (Robot Operating System) isn't really an operating system — it's a
messaging framework that lets many small programs ("nodes") talk to each
other, usually spread across a robot's different sensors, motors, and
brains. The single most important pattern in ROS is **publish/subscribe**:
one node broadcasts data on a named "topic," and any number of other nodes
can listen in, with neither side needing to know the other exists.

This practical builds exactly that: one node that shouts "hello" once a
second, and one node that listens and prints what it hears. Once you've seen
this work, you've seen the core idea behind almost every ROS system, robots
included.

## A quick, honest note on macOS

ROS is built and tested for Ubuntu Linux. It is not officially supported on
macOS, and trying to install it directly on your Mac is a common source of
wasted afternoons. The standard fix — what real robotics labs do on
Mac-based dev machines — is to run ROS **inside a Docker container**, and
use VS Code's "Dev Containers" extension to edit and run code inside it as
if it were local. This works identically whether your 2022 MacBook is
Apple Silicon (M1 Pro/M2) or Intel; Docker pulls the right image for your
chip automatically.

## Step 0: One-time setup

1. Install **Docker Desktop for Mac**: https://www.docker.com/products/docker-desktop/
   Open it once after installing so it finishes its first-time setup.
2. Install **VS Code**: https://code.visualstudio.com/
3. In VS Code, install the **Dev Containers** extension (search
   `ms-vscode-remote.remote-containers` in the Extensions panel).

## Step 1: Get the project open

1. Unzip the project folder you were given (`hello_ros/`) somewhere on your
   Mac, and open that folder in VS Code (`File > Open Folder...`).
2. VS Code should pop up a notification: *"Folder contains a Dev Container
   configuration file. Reopen folder to develop in a container?"* — click
   **Reopen in Container**.
   - If you don't see the prompt, open the Command Palette
     (`Cmd+Shift+P`) and run **Dev Containers: Reopen in Container**.
3. The first run will take a few minutes: Docker is downloading a full
   Ubuntu + ROS 2 image. Subsequent opens are fast, since it's cached.
4. You'll know it worked when the blue box in the bottom-left corner of VS
   Code says something like `Dev Container: ROS 2 Jazzy Hello World`.

## Step 2: Sanity-check ROS is alive (no code required)

Open a terminal in VS Code (`` Ctrl+` ``) and run ROS's own built-in demo
nodes, just to confirm the environment itself works before we touch any of
our own code:

```bash
ros2 run demo_nodes_py talker
```

You should see it printing `Publishing: "Hello World: 0"` once a second.
Leave it running, open a **second** terminal (the `+` icon in the terminal
panel), and run:

```bash
ros2 run demo_nodes_py listener
```

You should see the listener printing `I heard: "Hello World: 0"` in step
with the talker. Stop both with `Ctrl+C` — this confirmed your setup is
solid, so if anything goes wrong from here, it's the code, not the
environment.

## Step 3: Run our own hello world

Now the two files we actually wrote: `talker.py` and `listener.py`. Open
both in the VS Code editor and read through the comments first — the
comments explain *why* each line exists, not just what it does.

In one terminal:

```bash
python3 talker.py
```

In a second terminal:

```bash
python3 listener.py
```

You should see the talker logging `Publishing: "Hello, ROS! (message #N)"`
once a second, and the listener logging `Heard: "Hello, ROS! (message #N)"`
right after each one. Stop either with `Ctrl+C`.

Notice: we never called `on_message()` or `publish_hello()` ourselves —
ROS calls them for us, on its own schedule (the timer) or in reaction to
incoming data (the subscription). That handoff of control to the framework
is the main mental shift when learning ROS.

## Check your understanding

1. What happens if you start `listener.py` *before* `talker.py`? What about
   the other way around? Why?
2. Open a third terminal and run `python3 listener.py` again, so two
   listeners are running at once. What happens? What does this tell you
   about how many subscribers a topic can have?
3. In `talker.py`, change `self.create_timer(1.0, ...)` to `0.2`. What
   changes when you rerun it?
4. Run `ros2 topic list` in a new terminal while talker.py is running. Then
   try `ros2 topic echo /hello_topic` — this is ROS's own built-in listener,
   with no code of yours involved at all. What does that tell you about what
   a "topic" actually is?

## Where this goes next (not needed today)

- Right now `talker.py` and `listener.py` are standalone scripts — real ROS
  code usually lives in a proper **package** (built with `colcon`), which
  matters once you want to share code or launch many nodes together with a
  single command via a *launch file*.
- The next natural step after this is usually a node that does something
  with the data instead of just printing it — e.g. subscribing to a number
  and republishing it doubled, which introduces both subscribing and
  publishing in the same node.

## One simplification worth knowing about

We skipped the `colcon build` / ROS package step entirely and just ran the
`.py` files directly with `python3`. This works because `rclpy` is a normal
importable Python library once ROS is sourced — but it means these scripts
can't be launched with `ros2 run` or combined into launch files the way a
proper package's nodes can. That's the right trade for a first hello world;
it's the first thing to unlearn once you move to a real project.
