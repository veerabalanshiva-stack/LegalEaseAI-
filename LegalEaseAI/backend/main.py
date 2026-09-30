from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from backend.routes import router


app = FastAPI(
    title="LegalEase AI Legal Document Generator",
    description="AI-assisted legal document drafting API",
    version=settings.APP_VERSION
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"]
)


app.include_router(router)


@app.get("/")
def home():

    return {
        "message": "Welcome to LegalEase AI Legal Document Generator API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "model": settings.GEMINI_MODEL,
        "gemini_configured": bool(
            settings.GEMINI_API_KEY
        )
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "legalEaseAPI.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )