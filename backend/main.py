import subprocess
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

from routers import auth
from routers import employees
from routers import competencies
from routers import assessments
from routers import roles
from routers import recommendations
from routers import materials
from routers import quizzes

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KarmaSkill AI",
    description=(
        "AI-powered Competency Gap and "
        "Personalized Learning Engine"
    ),
    version="0.1.0"
)

# Run seed.py automatically when the server starts
@app.on_event("startup")
def auto_seed_db():
    try:
        result = subprocess.run(["python", "seed.py"], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("Database seeded successfully on startup.")
        else:
            logger.warning(f"Database seed skipped or returned non-zero code: {result.stderr}")
    except Exception as e:
        logger.error(f"Failed to auto-seed database: {e}")

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",   # Vite default port
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:8090",
    "http://127.0.0.1:8090",
    "http://localhost:8091",
    "http://127.0.0.1:8091",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",  # matches all Vercel preview/prod deployments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(employees.router)
app.include_router(competencies.router)
app.include_router(assessments.router)
app.include_router(roles.router)
app.include_router(recommendations.router)
app.include_router(materials.router)
app.include_router(quizzes.router)


@app.get("/")
def root():
    return {
        "project": "KarmaSkill AI",
        "message": "Competency Gap Engine API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/api/seed-db")
def seed_database():
    """Manual endpoint to re-run seed.py from any web browser or HTTP client."""
    try:
        result = subprocess.run(["python", "seed.py"], capture_output=True, text=True)
        if result.returncode == 0:
            return {
                "status": "success",
                "message": "Database seeded successfully",
                "output": result.stdout
            }
        else:
            raise HTTPException(status_code=500, detail=f"Seed script error: {result.stderr}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))