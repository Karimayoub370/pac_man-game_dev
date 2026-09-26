```
# 👾 Pac-Man Ghost AI &amp; Movement Mechanics

In classic *Pac-Man*, the ghosts do not wander randomly; they move deterministically using **tile-based targeting** and **greedy distance minimization** [1-3].

---

## 🏃 How Ghost Navigation Works

As soon as a ghost enters a new tile in the maze, it calculates its next step [1]:

1. **No Backtracking**: Ghosts cannot execute a 180° turn during normal movement—they can only choose between moving straight, turning left, or turning right [1, 2].
2. **No Wall Collisions**: Directions that lead into solid walls are ignored [2].
3. **Distance Calculation**: The ghost measures the straight-line (Euclidean) distance from each eligible next tile to its active **Target Tile** and picks the path that gets it closest [2, 4].
4. **Tie-Breaker Rule**: If two paths are equal in distance, the ghost chooses based on a fixed directional priority: **UP &gt; LEFT &gt; DOWN** [2].

&gt; **State Switch Exception**: Ghosts execute an immediate 180° turn only when switching between behavioral modes (e.g., changing between Scatter, Chase, or Frightened states) [5, 6].

---

## 🎭 The 4 Ghost Behavior States

Ghosts alternate between four main states during gameplay [7, 8]:

- **Chase Mode**: The primary hunting state where each ghost updates its target tile based on its unique personality algorithm [6, 9].
- **Scatter Mode**: Ghosts briefly retreat to target fixed tiles in the four corners of the map [8, 10]:
  - 🔴 **Blinky**: Top-Right Corner [10]
  - 🩷 **Pinky**: Top-Left Corner [10]
  - 🩵 **Inky**: Bottom-Right Corner [10]
  - 🟠 **Clyde**: Bottom-Left Corner [10]
- **Frightened Mode**: Triggered when Pac-Man eats a Power Pellet. Ghosts turn blue, turn around, and pick paths at random using a pseudorandom number generator [5, 11].
- **Eaten Mode**: When caught, ghosts turn into eyes and target the tile directly in front of the Ghost House door to respawn [5, 6].

---

## 👻 Chase Mode Targeting Strategies

Every ghost calculates its target tile differently during Chase Mode [9]:

### 🔴 Blinky (Red) – "Shadow"
- **Target Tile**: Pac-Man's exact current location [9].
- **Behavior**: Relentless pursuer that trails directly behind Pac-Man [9].

### 🩷 Pinky (Pink) – "Speedy"
- **Target Tile**: 4 tiles ahead of Pac-Man's current direction [12].
- **Coding Bug**: When Pac-Man faces **UP**, a memory overflow bug shifts her target 4 tiles UP and 4 tiles LEFT [12-14].
- **Behavior**: Ambusher that aims to cut Pac-Man off from the front [15].

### 🩵 Inky (Cyan) – "Bashful"
- **Target Tile**: Finds a spot 2 tiles ahead of Pac-Man (or 2 UP + 2 LEFT if facing UP) [16], draws an imaginary vector from Blinky to that spot, and doubles its length [17].
- **Behavior**: Flanker that coordinates with Blinky to trap Pac-Man [17].

### 🟠 Clyde (Orange) – "Pokey"
- **Target Tile**: Targets Pac-Man directly when more than 8 tiles away [18]. As soon as he gets within 8 tiles, he switches his target back to his Scatter corner in the bottom-left [18].
- **Behavior**: Fickle pursuer that approaches Pac-Man from a distance but retreats when close [18].

``````
# 👾 Pac-Man Ghost AI &amp; Movement Mechanics

In classic *Pac-Man*, the ghosts do not wander randomly; they move deterministically using **tile-based targeting** and **greedy distance minimization** [1-3].

---

## 🏃 How Ghost Navigation Works

As soon as a ghost enters a new tile in the maze, it calculates its next step [1]:

1. **No Backtracking**: Ghosts cannot execute a 180° turn during normal movement—they can only choose between moving straight, turning left, or turning right [1, 2].
2. **No Wall Collisions**: Directions that lead into solid walls are ignored [2].
3. **Distance Calculation**: The ghost measures the straight-line (Euclidean) distance from each eligible next tile to its active **Target Tile** and picks the path that gets it closest [2, 4].
4. **Tie-Breaker Rule**: If two paths are equal in distance, the ghost chooses based on a fixed directional priority: **UP &gt; LEFT &gt; DOWN** [2].

&gt; **State Switch Exception**: Ghosts execute an immediate 180° turn only when switching between behavioral modes (e.g., changing between Scatter, Chase, or Frightened states) [5, 6].

---

## 🎭 The 4 Ghost Behavior States

Ghosts alternate between four main states during gameplay [7, 8]:

- **Chase Mode**: The primary hunting state where each ghost updates its target tile based on its unique personality algorithm [6, 9].
- **Scatter Mode**: Ghosts briefly retreat to target fixed tiles in the four corners of the map [8, 10]:
  - 🔴 **Blinky**: Top-Right Corner [10]
  - 🩷 **Pinky**: Top-Left Corner [10]
  - 🩵 **Inky**: Bottom-Right Corner [10]
  - 🟠 **Clyde**: Bottom-Left Corner [10]
- **Frightened Mode**: Triggered when Pac-Man eats a Power Pellet. Ghosts turn blue, turn around, and pick paths at random using a pseudorandom number generator [5, 11].
- **Eaten Mode**: When caught, ghosts turn into eyes and target the tile directly in front of the Ghost House door to respawn [5, 6].

---

## 👻 Chase Mode Targeting Strategies

Every ghost calculates its target tile differently during Chase Mode [9]:

### 🔴 Blinky (Red) – "Shadow"
- **Target Tile**: Pac-Man's exact current location [9].
- **Behavior**: Relentless pursuer that trails directly behind Pac-Man [9].

### 🩷 Pinky (Pink) – "Speedy"
- **Target Tile**: 4 tiles ahead of Pac-Man's current direction [12].
- **Coding Bug**: When Pac-Man faces **UP**, a memory overflow bug shifts her target 4 tiles UP and 4 tiles LEFT [12-14].
- **Behavior**: Ambusher that aims to cut Pac-Man off from the front [15].

### 🩵 Inky (Cyan) – "Bashful"
- **Target Tile**: Finds a spot 2 tiles ahead of Pac-Man (or 2 UP + 2 LEFT if facing UP) [16], draws an imaginary vector from Blinky to that spot, and doubles its length [17].
- **Behavior**: Flanker that coordinates with Blinky to trap Pac-Man [17].

### 🟠 Clyde (Orange) – "Pokey"
- **Target Tile**: Targets Pac-Man directly when more than 8 tiles away [18]. As soon as he gets within 8 tiles, he switches his target back to his Scatter corner in the bottom-left [18].
- **Behavior**: Fickle pursuer that approaches Pac-Man from a distance but retreats when close [18].

```

---