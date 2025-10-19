import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
load_dotenv(Path("D:/repos/weather-api/.env"))
print(os.getenv("KEY"))