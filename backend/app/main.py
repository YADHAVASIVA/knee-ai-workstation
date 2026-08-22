from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import engine, Base, SessionLocal
from app.db.seed.demo_implants import seed_demo_implants

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Knee AI Analysis backend...")
    settings.create_dirs()
    
    # Initialize DB tables
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    
    # Seed demo data
    logger.info("Seeding demonstration implant database...")
    db = SessionLocal()
    try:
        seed_demo_implants(db)
    finally:
        db.close()

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    from fastapi.responses import JSONResponse
    return JSONResponse(status_code=500, content={"detail": "Internal server error."})
