"""Run FastAPI server."""
import uvicorn
from src.config import load_config

config = load_config()
uvicorn.run("api.app:app", host=config.api_host, port=config.api_port, reload=True)
