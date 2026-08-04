from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "event_management.db"

DATE_FORMAT = "%Y-%m-%d %H:%M"
DISPLAY_DATE_FORMAT =  "%B %d, %Y at %I:%M %p"
LOG_LEVEL = "INFO"
LOG_FORMAT =  "%(asctime)s - %(name)s - %(levelname)s - %(message)s"