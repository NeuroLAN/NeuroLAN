import os
from pathlib import Path
import json
import subprocess

if __name__ == "__main__":
    print("Initializing environment...")

    db_path = os.path.join(Path(__file__).parent, ".db")
    users_db = os.path.join(db_path, "users.json")

    os.mkdir(db_path)
    
    with open(users_db, 'w') as f:
        json.dump({}, f, indent=4)

    subprocess.run([
        "python3", "-m", "venv", ".venv"
    ])

    subprocess.run([
        "pip", "install", "-r", "requirements.txt"
    ])

    print("Initializion finished.")
