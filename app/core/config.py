from pathlib import Path
from pydantic import BaseSettings
import yaml
import os

LOCAL_ROOT_DIR = str(Path(__file__).parent.parent)
DEFAULT_CONFIG_PATH = "/var/app"
DEFAULT_RELATIVE_CONFIG_PATH = "config/parameters.yml"
CONFIG_PATH = os.path.join(LOCAL_ROOT_DIR, DEFAULT_RELATIVE_CONFIG_PATH)

with open(CONFIG_PATH) as f:
    service_parameters = yaml.safe_load(f)

class GlobalSettings(BaseSettings):
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    PROJECT_NAME: str = "ml-model"
    PREFIX: str = "/api/v1"

class DevSettings(GlobalSettings):
    APP_ENV = "dev"
    DEBUG: bool = True
    REMOTE_MODEL_NAME: str = os.path.join(LOCAL_ROOT_DIR, "artifacts/model.pkl")
    ROLLBAR_TOKEN_SECRET_KEY: str = 'token'
    ROLLBAR_ENV_SECRET_KEY: str = 'environment'
    AUTH_TOKEN_HEADER_KEY: str = 'Auth'
    AUTH_TOKEN_SECRET_KEY: str = 'secret'
    NEWRELIC_APPNAME: str = 'appname'
    NEWRELIC_LICENSE: str = 'license'
    NEWRELIC_TRACING_ENABLED: bool = True
    DB_URL: str = "sqlite+aiosqlite:///test.db"

class ProdSettings(GlobalSettings):
    APP_ENV = "prod"
    DEBUG: bool = False
    BUCKET_NAME = ""
    REMOTE_MODEL_NAME = ""

settings_by_name = dict(
    dev=DevSettings(),
    prod=ProdSettings()
)

settings = settings_by_name['dev']
LOGGING_LEVEL = "debug" if settings.DEBUG else "info"
