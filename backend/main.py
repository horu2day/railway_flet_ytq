from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import auth_routes, youtube_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix="/api/auth", tags=["auth"])
app.include_router(youtube_routes.router, prefix="/api/youtube", tags=["youtube"])