from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from views import video as video_view
from views import user as user_view
from utils import config

API_CONFIG = config.get("fastapi", {})
REDIS_CONFIG = config.get("redis", {})

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=API_CONFIG.get("allow_origins", ["*"]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video_view.router, prefix=API_CONFIG.get("prefix", "/api/v1"))
app.include_router(user_view.router, prefix=API_CONFIG.get("prefix", "/api/v1"))

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        "main:app",
        host=API_CONFIG.get("host", "127.0.0.1"),
        port=API_CONFIG.get("port", 8000),
        # reload=True,
        # workers=1
    )
