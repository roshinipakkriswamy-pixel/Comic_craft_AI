
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import router


BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="ComicCraft - AI Comic Story Creator",
    description="AI-powered comic story and illustration generator",
    version="1.0.0",
)


# Static files
static_dir = BASE_DIR / "static"
static_dir.mkdir(exist_ok=True)

app.mount(
    "/static",
    StaticFiles(directory=str(static_dir)),
    name="static",
)


# API routes
app.include_router(router)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "ComicCraft is running!"
    }

