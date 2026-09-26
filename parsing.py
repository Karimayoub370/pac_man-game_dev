

from pathlib import Path
from typing import List, Union
from pydantic import BaseModel, Field, model_validator
import sys

database = {
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

class Level(BaseModel):
    level_id: int = Field(1, ge=1)
    width: int = Field(1, ge=1)
    height: int = Field(1, ge=1)
    pacgum: int = Field(0, ge=0)


class GameData(BaseModel):
    highscore_filename: str
    lives: int = Field(1, ge=1)
    seed: int = Field(1, ge=1)
    level_max_time: int = Field(1, ge=1)
    points_per_pacgum: int = Field(0, ge=0)
    points_per_super_pacgum: int = Field(0, ge=0)
    points_per_ghost: int = Field(0, ge=0)
    levels: List[Level]

    @model_validator(mode="before")
    @classmethod
    def parse_values(cls, values):
        values["lives"] = max(1, values.get("lives", 1))
        values["seed"] = max(1, values.get("seed", 1))
        values["level_max_time"] = max(1, values.get("level_max_time", 1))

        values["points_per_pacgum"] = max(0, values.get("points_per_pacgum", 0))
        values["points_per_super_pacgum"] = max(0, values.get("points_per_super_pacgum", 0))
        values["points_per_ghost"] = max(0, values.get("points_per_ghost", 0))

        for level in values.get("levels", []):
            level["level_id"] = max(1, level.get("level_id", 1))
            level["width"] = max(1, level.get("width", 1))
            level["height"] = max(1, level.get("height", 1))
            level["pacgum"] = max(0, level.get("pacgum", 0))

        return values



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
        data = GameData.model_validate_json(json_content)
        assert len(data.levels) > 0, "Validation failed: levels list is empty"

    except Exception as e:
        print("Validation error while parsing the JSON file, use default database instead")
        return GameData.model_validate(database)
    return data


def main(file_path: Union[str, Path] = "filetest.json") -> GameData:
    """Test parsing the JSON file and print the validated data."""
    print(f"Testing parsing for '{file_path}'...")
    data = load_game_data(file_path)
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