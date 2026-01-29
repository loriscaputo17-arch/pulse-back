from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.gcp import setup_gcp_credentials
from app.api.router import api_router


# =========================
# Init GCP credentials
# =========================
setup_gcp_credentials()


# =========================
# Debug (safe)
# =========================
print("GCP CREDS:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    print(
        "FILE EXISTS:",
        os.path.exists(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    )


# =========================
# FastAPI app
# =========================
app = FastAPI(title="Pulse Back")


# =========================
# CORS
# =========================
origins = [
    "http://localhost:3000",
    "https://pulse-dashboard-black.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# Routes
# =========================
app.include_router(api_router)


# =========================
# Health check (Render)
# =========================
@app.get("/healthz")
def healthz():
    return {"status": "ok"}
