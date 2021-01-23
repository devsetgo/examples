import logging
from pathlib import Path

from loguru import logger
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

# set log level [DEBUG, INFO, WARNING, ERROR, CRITICAL]
LOGURU_LOGGING_LEVEL = "DEBUG"

def config_log():
    
     # remove default logger
    logger.remove()
    # set file path
    log_path = Path.cwd().joinpath("log").joinpath("app_log.log")
    # add new configuration
    logger.add(
        log_path, #log file path
        level=LOGURU_LOGGING_LEVEL, #logging level
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", #format of log
        enqueue=True, # set to true for async or multiprocessing logging
        backtrace=False, # turn to false if in production to prevent data leaking
        rotation="10 MB", #file size to rotate
        retention="10 Days", # how long a the logging data persists
        compression="zip", # log rotation compression
        serialize=False, # if you want it JSON style, set to true. But also change the format
    )
    
    #intercept standard logging
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    logging.basicConfig(handlers=[InterceptHandler()], level=0)


def start_up():
    config_log()

async def index_route(request):
    logging.debug("logging")
    logger.debug("logger")
    logging.info("logging")
    logger.info("logger")
    logging.warning("logging")
    logger.warning("logger")
    logging.error("logging")
    logger.error("logger")
    logging.critical("logging")
    logger.critical("logger")

    return JSONResponse({"status": "UP"})

app = Starlette(on_startup=[start_up],routes=[
    Route('/', index_route),
])


if __name__ == "__main__":
    import uvicorn

    # logging has to be lower case for Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, debug=False, log_level=LOGURU_LOGGING_LEVEL.lower()) 