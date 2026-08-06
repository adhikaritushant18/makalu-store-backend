import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.database import Base, engine
from app.models import *
from app.router.partner import router as partner_router
from app.router.partner_equipment import router as partner_equipment_router
from app.router.partner_assignment import router as partner_assignment_router
from app.router.partner_return import router as partner_return_router
from app.router.partner_receive import router as partner_receive_router

from app.router import (
    assignment_router,
    category_router,
    dashboard_router,
    equipment_router,
    location_router,
)

load_dotenv()

Base.metadata.create_all(bind=engine)

root_path = os.getenv("ROOT_PATH", "")

default_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://makalu-store-frontend.vercel.app",
]
cors_origins = os.getenv("CORS_ORIGINS")
origins = (
    [origin.strip() for origin in cors_origins.split(",") if origin.strip()]
    if cors_origins
    else default_origins
)

app = FastAPI(
    title="Makalu Store Management API",
    version="0.1.0",
    root_path=root_path,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Makalu Store Management API"
    }


app.include_router(category_router)
app.include_router(location_router)
app.include_router(equipment_router)
app.include_router(assignment_router)
app.include_router(dashboard_router)
app.include_router(auth_router)
app.include_router(partner_router)
app.include_router(partner_equipment_router)
app.include_router(partner_assignment_router)
app.include_router(partner_return_router)
app.include_router(partner_receive_router)
