from pathlib import Path
from typing import List, Union
from pydantic import BaseModel, Field
import sys


class Level(BaseModel):
    level_id: int
    width: int
    height: int
    pacgum: int


class GameData(BaseModel):
    highscore_filename: str
    lives: int
    seed: int
    level_max_time: int
    points_per_pacgum: int
    points_per_super_pacgum: int
    points_per_ghost: int
    levels: List[Level]


def strip_comments_from_line(line: str) -> str:
    """Remove comments starting with '#' from a line, preserving '#' inside strings."""
    in_string = False
    escape = False
    for i, char in enumerate(line):
        if char == '"' and not escape:
            in_string = not in_string
        elif char == "\\" and in_string:
            escape = not escape
            continue
        elif char == "#" and not in_string:
            return line[:i] + "\n"
        escape = False
    return line


def load_game_data(file_path: Union[str, Path] = "filetest.json") -> GameData:
    """Parse and validate a JSON configuration file into a GameData model,
    stripping comments starting with '#' before JSON decoding.
    """
    path = Path(file_path)
    cleaned_lines = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            cleaned_line = strip_comments_from_line(line)
            cleaned_lines.append(cleaned_line)

    json_content = "".join(cleaned_lines)

    if hasattr(GameData, "model_validate_json"):
        return GameData.model_validate_json(json_content)
    return GameData.parse_raw(json_content)


def main(file_path: Union[str, Path] = "filetest.json") -> GameData:
    """Test parsing the JSON file and print the validated data."""
    print(f"Testing parsing for '{file_path}'...")
    data = load_game_data(file_path)
    assert isinstance(
        data, GameData
    ), "Validation failed: data is not an instance of GameData"
    assert len(data.levels) > 0, "Validation failed: levels list is empty"
    print("Parsing successful!")
    print(f"Highscore File: {data.highscore_filename}")
    print(f"Lives: {data.lives}, Seed: {data.seed}, Max Time: {data.level_max_time}s")
    print(f"Levels ({len(data.levels)}):")
    for lvl in data.levels:
        print(
            f"  - Level {lvl.level_id}: {lvl.width}x{lvl.height} (pacgums: {lvl.pacgum})"
        )
    return data


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
