from fastapi import Depends, HTTPException, Header
from jose import jwt

# Usa la tua chiave segreta di Supabase
SUPABASE_JWT_SECRET = "S04bVOsB7B0B4D3Xor6y71HT09TSNS1ZauZfxIVzI3ukRdHZIvu+ASrvpvDP11cDJNlvLIuiGlAUVgnYO2zAGw=="

def get_current_user_id(authorization: str = Header(None)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Token mancante")
    
    try:
        token = authorization.split(" ")[1]
        # Decodifica il token e verifica la firma
        payload = jwt.decode(
            token, 
            SUPABASE_JWT_SECRET, 
            algorithms=["HS256"], 
            audience="authenticated"
        )
        # 'sub' è l'UID dell'utente in Supabase
        return payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Token non valido o scaduto")