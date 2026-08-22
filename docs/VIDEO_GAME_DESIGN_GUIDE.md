# Video game design guide

Open Organism is "affect-driven" — Embryo-Zero already turns sensor state
(temperature, load) into a mood (see [VISION.md](../VISION.md) and
[ROADMAP.md](ROADMAP.md) Phase 1). A natural companion project is a small
game or interactive visualizer that lets a person see, and play with, the
organism's inner state — a digital-pet-style front end for a physical
device. This guide covers the game design knowledge needed to build that,
and applies generally to any small game built alongside this project.

## 1. Core design concepts

- **Core loop** — the small cycle of action → feedback → decision the
  player repeats. For an organism companion: *observe mood → feed/adjust
  input → see mood change → decide what to do next.* Get this loop fun
  and legible before adding anything else.
- **Game feel / juice** — the immediate feedback (animation, sound,
  screen shake, particles) that makes an action feel responsive. Even a
  simple LED-blink-to-screen-pulse mapping benefits from smoothing,
  easing, and a slight delay/overshoot rather than an instant snap.
- **State machine** — most simple games (and Embryo-Zero's mood system)
  are best modeled as explicit states (calm, stressed, curious, hungry)
  with defined transitions, rather than free-form logic. This mirrors
  the mood model already implicit in the roadmap.
- **Difficulty / pacing curve** — if the game has any challenge element
  (e.g. "keep the organism's stress low"), design the pacing so the
  player is challenged but not overwhelmed; introduce mechanics one at a
  time.
- **Readability first** — a player should always be able to tell, at a
  glance, what state the system is in and what their options are. This
  matters even more for a game that's a proxy for a real physical device
  — misleading feedback breaks trust in the device, not just the game.

## 2. Game loop architecture (technical)

A real-time game (including a live organism dashboard) runs a loop:

```
while running:
    input = read_input()          # player input, or sensor data over the network
    update(state, input, dt)      # advance simulation by delta-time
    render(state)                 # draw the current frame
```

- **Fixed vs. variable timestep** — for anything with physics or
  consistent simulation speed, decouple `update()` from frame rate using
  a fixed timestep accumulator so behavior doesn't change with framerate.
  For a mood/state visualizer driven by sensor polling, a simpler
  variable-timestep loop is usually fine since there's no physics to
  destabilize.
- **Separation of simulation and rendering** — keep the organism's
  actual state (mirroring or reading from the real device / UCP
  protocol, see [UCP_SPEC.md](../UCP_SPEC.md)) separate from how it's
  drawn. This lets you swap visuals without touching the simulation, and
  lets the same state feed multiple views (a 2D sprite, a simple 3D
  blob, a text log).

## 3. Genres and structures worth knowing

- **Simulation / life-sim (Tamagotchi, Creatures, Stardew Valley pet
  systems)** — closest fit for an organism companion. Core mechanics:
  needs that decay over time, player actions that satisfy needs, and
  visible state changes (mood, appearance, animation).
  - Simplification for a companion prototype: it doesn't need scoring or
    a win condition, just a legible state and interesting-enough
    interactions to make checking in worthwhile.
- **Idle / incremental** — useful pattern if the organism accumulates
  something over time (uptime, "experience", mesh connections) even
  while the player isn't watching. Good fit for the "planetary nervous
  system" long-term vision.
- **Puzzle / arcade** — not a natural fit here, but worth knowing the
  vocabulary (win/lose states, score, levels) in case a minigame
  (e.g. "stabilize the organism's temperature") gets added later.

## 4. Data-driven design

- Define moods, thresholds, and transitions in a small config file/table
  (JSON, YAML, or a simple Python dict) rather than hardcoding them in
  logic. This mirrors how `embryo_zero.py` should expose its mood
  thresholds, and lets the visualizer and firmware share one source of
  truth for what each mood means.
- Keep the sensor→mood mapping and the mood→visual mapping as two
  separate, swappable layers, so the visualizer can change look without
  touching sensor logic, and the firmware can change thresholds without
  touching the UI.

## 5. Practical stack for a first prototype

- **Web-based (recommended for this project)**: HTML/CSS/JS or a small
  React app. Easiest to share, easiest to host next to the "public
  dashboard showing the organism state" stretch goal already in
  ROADMAP.md, and can read live data over a simple HTTP/WebSocket
  endpoint from the device.
- **Pygame (Python)**: fits naturally since firmware is already Python
  (`embryo_zero.py`); good for a local desktop visualizer without
  needing a web server.
- **Godot**: if the visualizer grows into something more game-like
  (animated creature, multiple screens, sound), Godot is free, open
  source, lightweight, and exports to web/desktop — a natural choice
  for an open-hardware/open-software project that already favors open
  tools (KiCad, MIT/CERN OHL licensing).

## 6. Suggested first build

1. Have `embryo_zero.py` (or a small wrapper) expose current sensor
   readings and computed mood as a simple JSON payload (local file or
   tiny HTTP endpoint).
2. Build a minimal front end (web page or Pygame window) that polls that
   payload and renders: current mood label, a simple animated
   indicator (color/shape change), and a short history sparkline.
3. Add one player interaction (e.g. a "check on it" button that requests
   a fresh reading, or a simple soothing action if the mood is
   "stressed") to close the core loop.
4. Only after that loop feels good, consider expanding into the
   idle/accumulation mechanics tied to uptime or mesh connections from
   later roadmap phases.

## 7. Further reading

- "A Game Design Vocabulary" by Anna Anthropy & Naomi Clark — grounding
  in core loop / verb / state vocabulary
- "Game Feel" by Steve Swink — for the juice/feedback layer
- Godot documentation "Your first 2D game" — practical, free tutorial
  matching the recommended stack above
