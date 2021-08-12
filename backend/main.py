import os

import uvicorn
from dotenv import load_dotenv, find_dotenv

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    # Configure logging behaviour
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"

    uvicorn.run("app:app", port=8000, host="0.0.0.0", reload=True, reload_dirs=["../scanners", "."], log_config=log_config)
