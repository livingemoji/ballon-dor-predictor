from fastapi import FastAPI

from api.routes import router
from db.database import engine
from db.models import Base


def create_app() -> FastAPI:
    app = FastAPI(title="Ballon d'Or Predictor API")
    app.include_router(router, prefix="/api")
    return app


app = create_app()


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
