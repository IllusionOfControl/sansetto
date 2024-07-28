from fastapi import FastAPI
from app.api import router as api_router


def get_app() -> FastAPI:
    app = FastAPI(
        title="tagger",
        description="tagger microservice",
        version="1.0.0"
    )

    app.include_router(api_router)

    return app


app = get_app()
