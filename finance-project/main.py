import logging
from fastapi import FastAPI, Request
from fastapi_utils.tasks import repeat_every
from api.users import users_router
from api.assets import assets_router
from domain.exceptions import (
    NonExistentUserId,
    InvalidTicker,
    DuplicateUser,
    DuplicateAsset,
)
from domain.user.factory import InvalidUsername
from starlette.responses import JSONResponse
import subprocess
import os
import time

logging.basicConfig(
    filename="finance.log",
    level=logging.DEBUG,
    format="%(asctime)s _ %(levelname)s _ %(name)s _ %(message)s",
)


app = FastAPI(
    debug=True,
    title="Fintech Portfolio API",
    description="A webserver with a REST API for keeping track of your different financial assets,"
    " stocks & crypto, and see/compare their evolution",
    version="1.0.0",
)

app.include_router(users_router)
app.include_router(assets_router)


@app.exception_handler(DuplicateAsset)
def return_duplicate_asset(_: Request, e: DuplicateAsset):
    logging.error(str(e))
    return JSONResponse(status_code=409, content=str(e))


@app.exception_handler(DuplicateUser)
def return_duplicate_user(_: Request, e: DuplicateUser):
    logging.warning(str(e))
    return JSONResponse(status_code=409, content=str(e))


@app.exception_handler(InvalidUsername)
def return_invalid_username(_: Request, e: InvalidUsername):
    invalid_username_error = "Username is not valid! Error: " + str(e)
    logging.error(invalid_username_error)
    return JSONResponse(status_code=400, content=invalid_username_error)


@app.exception_handler(NonExistentUserId)
def return_invalid_id(_: Request, e: NonExistentUserId):
    invalid_id_error = str(e)
    logging.error(invalid_id_error)
    return JSONResponse(status_code=404, content=invalid_id_error)


@app.exception_handler(InvalidTicker)
def return_invalid_ticker(_: Request, e: InvalidTicker):
    logging.error(str(e))
    return JSONResponse(status_code=404, content=str(e))


@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 24)
def clean_images_older_than_24h():
    files = os.listdir(".")
    graphs = [f for f in files if f.endswith(".png")]
    current_posix_time = time.time()
    ago_24h = current_posix_time - 60 * 60 * 24
    for g in graphs:
        g_creation_time = os.path.getctime(g)
        if g_creation_time < ago_24h:
            os.remove(g)


if __name__ == "__main__":
    logging.info("Starting webserver...")
    try:
        subprocess.run(["uvicorn", "main:app", "--reload"])
    except KeyboardInterrupt as e:
        logging.warning("Keyboard interrupt")
    except Exception as e:
        logging.warning("Webserver has stopped. Reason: " + str(e))
