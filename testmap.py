"""Minimal autonomous ghost pursuit prototype."""

from __future__ import annotations
import math

# Grid definitions: 1 = Wall, 0 = Corridor
TEST_MAP: list[list[int]] = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Direction vectors: (delta_row, delta_col)
DIRECTIONS: dict[str, tuple[int, int]] = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}

OPPOSITES: dict[str, str] = {
    "UP": "DOWN",
    "DOWN": "UP",
    "LEFT": "RIGHT",
    "RIGHT": "LEFT",
    "NONE": "NONE",
}


def distance_sq(pos_a: tuple[int, int], pos_b: tuple[int, int]) -> float:
    """Calculate squared Euclidean distance between two grid points."""
    return (pos_a[0] - pos_b[0]) ** 2 + (pos_a[1] - pos_b[1]) ** 2


class Ghost:
    """Represents an autonomous ghost entity."""

    def __init__(self, start_pos: tuple[int, int]) -> None:
        """Initialize ghost with starting grid coordinates."""
        self.pos: tuple[int, int] = start_pos
        self.current_direction: str = "NONE"

    def get_valid_moves(self, grid: list[list[int]]) -> list[tuple[str, tuple[int, int]]]:
        """Find adjacent corridor tiles excluding direct 180 reversals."""
        valid: list[tuple[str, tuple[int, int]]] = []
        rows, cols = len(grid), len(grid[0])

        for direction, (dr, dc) in DIRECTIONS.items():
            # Disallow immediate 180-degree turnaround
            if direction == OPPOSITES.get(self.current_direction):
                continue

            nr, nc = self.pos[0] + dr, self.pos[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                valid.append((direction, (nr, nc)))

        # Fallback: if trapped in a dead end, allow reversing
        if not valid and self.current_direction in OPPOSITES:
            rev_dir = OPPOSITES[self.current_direction]
            dr, dc = DIRECTIONS[rev_dir]
            nr, nc = self.pos[0] + dr, self.pos[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                valid.append((rev_dir, (nr, nc)))

        return valid

    def step(self, target_pos: tuple[int, int], grid: list[list[int]]) -> None:
        """Evaluate surroundings and make one autonomous move toward target."""
        valid_moves = self.get_valid_moves(grid)
        if not valid_moves:
            return

        # Pick the valid adjacent tile that minimizes distance to the target
        best_direction, best_pos = min(
            valid_moves,
            key=lambda move: distance_sq(move[1], target_pos),
        )

        self.current_direction = best_direction
        self.pos = best_pos


def render_scene(grid: list[list[int]], player: tuple[int, int], ghost: tuple[int, int]) -> None:
    """Print the ASCII board to stdout."""
    symbols = {1: "#", 0: " "}
    for r, row in enumerate(grid):
        line = []
        for c, cell in enumerate(row):
            if (r, c) == player:
                line.append("P")
            elif (r, c) == ghost:
                line.append("G")
            else:
                line.append(symbols[cell])
        print("".join(line))
    print("-" * len(grid[0]))


if __name__ == "__main__":
    # Setup initial positions
    player_position = (3, 4)  # Center of the map
    ghost_entity = Ghost(start_pos=(1, 1))  # Top-left corner

    print("Initial Board (P = Player, G = Ghost, # = Wall):")
    render_scene(TEST_MAP, player_position, ghost_entity.pos)

    # Simulate 5 autonomous steps
    for step_num in range(1, 6):
        ghost_entity.step(target_pos=player_position, grid=TEST_MAP)
        print(f"Step {step_num} (Ghost moved {ghost_entity.current_direction}):")
        render_scene(TEST_MAP, player_position, ghost_entity.pos)