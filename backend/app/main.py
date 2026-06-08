from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from app.core.config import settings
from app.api.routes import auth
import os

load_dotenv()

app = FastAPI(
    title=settings.APP_NAME,
    description="API for connecting brands and influencers",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for uploads
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Routes
app.include_router(auth.router)

@app.get("/")
def root():
    return {
        "message": f"{settings.APP_NAME} API is running",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}