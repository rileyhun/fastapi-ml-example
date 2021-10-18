from pathlib import Path
from app.core.config import LOGGING_LEVEL

BASE_DIR = Path(__file__).resolve().parent.parent

LOGGER = {
    "path": str(Path(BASE_DIR / 'log/access.log')),
    "level": LOGGING_LEVEL,
    "rotation": "20 days",
    "retention": "1 months",
    "format": "<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> - <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
}

