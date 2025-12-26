import random
import json

class RollerModel:
    # Handles backend data persistence and random number generation logic.
    def __init__(self):
        # Initialize an empty list to track character stats in memory.
        self.stats = []
    
    def roll_dice(self, count, faces):
        # Generates random results for a specified number of dice and face count.
        # Returns the total sum, individual roll results, and the face count.
        results = [random.randint(1, faces) for _ in range(count)]
        return sum(results), results, faces

    def save_stats_to_file(self, stats_data, filename="stats.json"):
        # Serializes character stat data into a local JSON file for persistence.
        with open(filename, "w") as f:
            json.dump(stats_data, f)

    def load_stats_from_file(self, filename="stats.json"):
        # Retrieves saved stats from JSON or provides default values if the file is missing.
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Default starting stats if no save file exists.
            return [{"name": "STR", "value": 11}, {"name": "DEX", "value": 12}]