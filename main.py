from dotenv import load_dotenv
load_dotenv()

import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.gcp import setup_gcp_credentials
from app.api.router import api_router


# =========================
# GCP CREDENTIALS (Render)
# =========================
# Se siamo su Render, GOOGLE_CREDENTIALS_JSON è settata
if "GOOGLE_CREDENTIALS_JSON" in os.environ:
    creds_path = "/tmp/gcp-service-account.json"

    with open(creds_path, "w") as f:
        json.dump(json.loads(os.environ["GOOGLE_CREDENTIALS_JSON"]), f)

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path


# =========================
# DEBUG (safe)
# =========================
print("GCP CREDS:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    print(
        "FILE EXISTS:",
        os.path.exists(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    )


# =========================
# Init GCP (BigQuery)
# =========================
setup_gcp_credentials()


# =========================
# FastAPI app
# =========================
app = FastAPI(title="Pulse Back")


# =========================
# CORS
# =========================
origins = [
    "http://localhost:3000",        # dev
    "https://tuo-frontend.com",     # prod (aggiungilo quando serve)
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
