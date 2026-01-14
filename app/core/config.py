from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
 
class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str

    GCP_PROJECT: str
    BQ_DATASET: str

    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = Field(default=None)

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
