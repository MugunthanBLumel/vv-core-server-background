import uvicorn
import logging

from app.core.logging import HubLogger
from app.fast_api import init_fast_api_app
from app.server_warmup import warm_up
from app.conf.worker import worker

logger = logging.getLogger(__name__)

# Validate and WarmUP
warm_up()

# Fast API INIT
app = init_fast_api_app(HubLogger.customize_logging())

# Main File
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
