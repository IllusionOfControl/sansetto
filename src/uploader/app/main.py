from app.api import router as api_router
from fastapi import FastAPI


def get_app() -> FastAPI:
    app = FastAPI(
        title="uploader", description="uploader microservice", version="1.0.0"
    )

    app.include_router(api_router)

    return app


app = get_app()
