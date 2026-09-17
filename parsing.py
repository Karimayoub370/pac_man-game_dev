from pathlib import Path
from typing import List, Union
from pydantic import BaseModel, Field


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


def load_game_data(file_path: Union[str, Path] = "filetest.json") -> GameData:
    """Parse and validate a JSON configuration file into a GameData model."""
    path = Path(file_path)
    with path.open("r", encoding="utf-8") as f:
        json_content = f.read()

    if hasattr(GameData, "model_validate_json"):
        return GameData.model_validate_json(json_content)
    return GameData.parse_raw(json_content)


def test_parsing(file_path: Union[str, Path] = "filetest.json") -> GameData:
    """Test parsing the JSON file and print the validated data."""
    print(f"Testing parsing for '{file_path}'...")
    data = load_game_data(file_path)
    assert isinstance(data, GameData), "Validation failed: data is not an instance of GameData"
    assert len(data.levels) > 0, "Validation failed: levels list is empty"
    print("Parsing successful!")
    print(f"Highscore File: {data.highscore_filename}")
    print(f"Lives: {data.lives}, Seed: {data.seed}, Max Time: {data.level_max_time}s")
    print(f"Levels ({len(data.levels)}):")
    for lvl in data.levels:
        print(f"  - Level {lvl.level_id}: {lvl.width}x{lvl.height} (pacgums: {lvl.pacgum})")
    return data


if __name__ == "__main__":
    test_parsing()