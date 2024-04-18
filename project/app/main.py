# project/app/main.py


import logging

from fastapi import FastAPI

from app.api import ping, summaries
from app.db import init_db


log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router)
    application.include_router(
        summaries.router, prefix="/summaries", tags=["summaries"])  # new

    return application


app = create_application()

"""
It's worth nothing that the startup and shutdown event handlers are deprecated 
in favor of lifespan async context managers. 

We're continuing to use the former since the register_tortoise helper isn't,
 as of writing, compatible with lifespan async context managers.

 """


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
