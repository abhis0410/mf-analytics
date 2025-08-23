import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Path to favourites JSON file
FAV_FILE_PATH = os.path.join(BASE_DIR, "data", "favourites.json")
BLACKLIST_FILE_PATH = os.path.join(BASE_DIR, "data", "blacklist.json")
SAVED_SIMULATIONS_FILE_PATH = os.path.join(BASE_DIR, "data", "saved_simulations.json")
MY_INVESTMENTS_FILE_PATH = os.path.join(BASE_DIR, "data", "my_investments.json")
