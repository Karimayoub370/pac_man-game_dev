from pathlib import Path
from typing import List, Union
from pydantic import BaseModel, Field, ValidationError
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


def load_game_data(file_path) -> GameData:
    """Parse and validate a JSON configuration file into a GameData model,
    stripping comments starting with '#' before JSON decoding.
    """
    res = {
    "highscore_filename": "highscores.json",
    "lives": 3,
    "seed": 42,
    "level_max_time": 90,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "levels": [
        {
            "level_id": 1,
            "width": 21,
            "height": 21,
            "pacgum": 42
        },
        {
            "level_id": 2,
            "width": 25,
            "height": 25,
            "pacgum": 60
        }
    ]
}
    path = Path(file_path)
    cleaned_lines = []
    try:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                cleaned_line = strip_comments_from_line(line)
                cleaned_lines.append(cleaned_line)
        json_content = "".join(cleaned_lines)
        GameData.model_validate_json(json_content)

    except ValidationError as e:
        print(f"Validation error while parsing '{file_path}': {e}")
        return GameData.model_validate(res)
        
    # if hasattr(GameData, "model_validate_json"):
    #     return GameData.model_validate_json(json_content)
    return GameData.model_validate_json(json_content)


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
    try:
        if len(sys.argv) == 2:
            main(sys.argv[1])
        else:
            main()
    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)