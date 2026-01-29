from dotenv import load_dotenv
load_dotenv()
import os
from fastapi import FastAPI
from app.core.gcp import setup_gcp_credentials
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router

print("GCP CREDS:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
print("FILE EXISTS:", os.path.exists(os.getenv("GOOGLE_APPLICATION_CREDENTIALS")))


setup_gcp_credentials()
app = FastAPI(title="Pulse Back")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
