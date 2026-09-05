import json
import os
import random

def get_random_map_name():
    return random.choice(["map_square.json", "map_triangle.json", "map_octagon.json"])

def load_raw_map_data(filename):
    filepath = os.path.join("assets", "maps", filename)
    with open(filepath, 'r') as f:
        return json.load(f)