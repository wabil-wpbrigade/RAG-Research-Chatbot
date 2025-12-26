from app.db import schemas
from fastapi import FastAPI
from app.db.database import engine
from app.db.seed import seed_admin
from contextlib import asynccontextmanager
from app.rag.routes import router as rag_router
from app.auth.routes import router as auth_router
from app.users.routes import router as users_router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1️⃣ Create DB tables
    schemas.Base.metadata.create_all(bind=engine)

    # 2️⃣ Seed default admin (idempotent)
    seed_admin()

    yield


app = FastAPI(
    title="Research RAG Backend",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3️⃣ Routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(rag_router)


@app.get("/health")
def health():
    return {"status": "ok"}
