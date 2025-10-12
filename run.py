"""
run.py

Entry point for the News Tracker application.
Ensures Docker services are running and starts the main Python app.
"""

import subprocess
import sys
from pathlib import Path
from src.logger import Logger

logger = Logger.get("Run")

def main():
    """Starts Docker services if available and runs the main app."""
    logger.info("Running application - News Tracker")

    docker_compose = Path(__file__).parent / "docker-compose.yml"
    if docker_compose.exists():
        logger.info("Ensuring Docker services are running...")
        subprocess.run(["docker", "compose", "up", "-d"], check=True)

    subprocess.run([sys.executable, "-m", "src.main"], check=True)

if __name__ == "__main__":
    main()
