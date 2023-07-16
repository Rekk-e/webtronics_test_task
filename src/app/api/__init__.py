from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api.routers.api import api_router
from app.db.init_db import init_db

def init_app() -> FastAPI:
    """
    Function to initialize the application
    """
    app = FastAPI()
    register_app(app)

    app.include_router(router=api_router, prefix="/api")

    return app

def register_db(app: FastAPI):
    """
    Function to start initialization the database
    """
    @app.on_event("startup")
    async def register_db_event():
        await init_db()

def register_openapi(app: FastAPI):
    """
    API registration function
    """
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="webtronics_task-api",
            version="1.0.0",
            description="",
            routes=app.routes,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi


def register_cors_middleware(app: FastAPI):
    """
    function registers middleware for Cross-Origin Resource Sharing (CORS).
    CORS allows web applications to communicate with each other when they are on different domains.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )


def register_app(app: FastAPI):
    """
    Additional function to initialize the application
    """
    register_cors_middleware(app)
    register_db(app)
    register_openapi(app)
