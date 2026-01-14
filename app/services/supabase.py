from supabase import create_client, Client
from app.core.config import settings
from typing import Optional

_supabase_admin: Optional[Client] = None

def get_supabase_admin() -> Client:
    global _supabase_admin

    if _supabase_admin is None:
        _supabase_admin = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_ROLE_KEY
        )

    return _supabase_admin
