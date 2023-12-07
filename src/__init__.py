from fastapi import FastAPI

from src.modules import api_router
from src.config.database import engine, Base

Base.metadata.create_all(bind=engine)


def init_app(app: FastAPI) -> FastAPI:
    app.include_router(api_router)
    return app
