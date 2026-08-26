# Part 2: a three-node pipeline (same devcontainer, no new setup)

## What's new here

The hello world had two nodes: one that only publishes, one that only
subscribes. Real ROS systems are usually longer chains, and the nodes in
the middle of the chain do both — they listen for data, transform it, and
pass the result on. That's the one new idea in this practical.

We build a three-node pipeline:

```
number_publisher  --"numbers"-->  doubler  --"doubled_numbers"-->  printer
     (publishes)                (subscribes AND publishes)        (subscribes)
```

`number_publisher.py` and `printer.py` are nothing new — they're the same
publish-only / subscribe-only shapes as `talker.py` and `listener.py`. All
the new ideas live in `doubler.py`.

These files go in the *same* `hello_ros/` project folder as before, using
the *same* dev container — no new setup required.

## Run it

Open three terminals in VS Code and run one command in each:

```bash
python3 number_publisher.py
```

```bash
python3 doubler.py
```

```bash
python3 printer.py
```

You should see three synchronized logs: `number_publisher` counting up,
`doubler` reporting `Received N, publishing 2N` for each one, and `printer`
showing `Final result: 2N`. Data is flowing through all three nodes,
transformed once along the way, and none of the three nodes has any
direct reference to either of the others — they only know topic names.

## See the wiring from the outside

With all three still running, open a fourth terminal:

```bash
ros2 topic list
```

You should see `/numbers` and `/doubled_numbers` — the two topics
connecting the pipeline. Try:

```bash
ros2 topic echo /numbers
```

and then, in another terminal:

```bash
ros2 topic echo /doubled_numbers
```

Neither of these commands is one of "our" nodes — `ros2 topic echo` is a
generic ROS tool that can listen to *any* topic, from *any* node, without
you writing a line of code. This is a good way to debug a pipeline: you can
eavesdrop on any point in the chain independently.

## Check your understanding

1. Change `doubler.py` to triple instead of double, and rerun just that one
   file (leave the other two running). How quickly does the change show up
   downstream, and why didn't you need to restart `number_publisher.py` or
   `printer.py`?
2. Start a second `printer.py` in a fourth terminal, so two printers are
   both subscribed to `doubled_numbers`. What happens? Does `doubler.py`
   publish twice as much data, or does it not know or care how many
   subscribers it has?
3. Kill `number_publisher.py` (Ctrl+C) while the other two keep running.
   What do `doubler.py` and `printer.py` do? What does this tell you about
   how tightly coupled — or not — these nodes are to each other?
4. Write a fourth node, `squarer.py`, that subscribes to `/numbers` and
   publishes the square of each value to a new topic, `/squared_numbers`.
   You now have one input topic feeding two independent downstream nodes —
   sketch (on paper or in the chat) what the resulting graph of nodes and
   topics looks like.

## Where this goes next

Running three (or four) separate terminals by hand doesn't scale. The next
real step in ROS is usually:

- Bundling nodes like these into a proper **package** built with `colcon`,
  which lets you start them with `ros2 run` instead of `python3`.
- Writing a **launch file** that starts every node in the pipeline with a
  single command, instead of one terminal per node.

Both are natural next practicals once this pattern — several small,
independent nodes wired together purely through topic names — feels
comfortable.
