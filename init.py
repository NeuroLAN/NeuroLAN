import subprocess
import os
from pathlib import Path

if __name__ == "__main__":
    print("Initializing environment...")
    
    venv_path = os.path.exists(Path(__file__).parent / ".venv")
    
    if not venv_path:
        subprocess.run([
            "python3", "-m", "venv", ".venv"
        ])

        subprocess.run([
            f"{venv_path}/bin/pip", "install", "-r", "requirements.txt"
        ])

    print("Initializion finished.")
    print("Please acctive your virtual environment.")