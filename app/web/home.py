from app.router import router
from app.config import Config


@router("/")
def index(config: Config):
    return f"It is a bot of telegram and its name is: {config.SERVICE_NAME}"
