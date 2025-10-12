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

def start():
    '''start'''
    logger.info("Starting News Tracker bot...")
    docker_compose = Path(__file__).parent / "docker-compose.yml"
    if docker_compose.exists():
        subprocess.run(["docker", "compose", "up", "-d"], check=True)
    subprocess.run([sys.executable, "-m", "src.main"], check=True)

def stop():
    '''stop'''
    logger.info("Stopping Docker services...")
    subprocess.run(["docker", "compose", "down"], check=True)

def main():
    '''Main'''
    if len(sys.argv) < 2:
        print("Usage: python run.py [start|stop]")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "start":
        start()
    elif cmd == "stop":
        stop()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
