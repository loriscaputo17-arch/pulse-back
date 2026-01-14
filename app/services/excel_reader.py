import pandas as pd

def read_artist_daily(path: str, sheet: str):
    df = pd.read_excel(path, sheet_name=sheet)
    df.columns = df.columns.str.lower().str.strip()

    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    for c in ["listeners", "streams", "followers", "saves"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    df["artist"] = sheet
    return df[["artist", "date", "listeners", "streams", "followers", "saves"]]

def read_artist_total(path: str, sheet="total"):
    df = pd.read_excel(path, sheet_name=sheet)
    df.columns = df.columns.str.lower().str.strip()

    row = df.iloc[:1].copy()
    row["ingested_at"] = pd.Timestamp.utcnow()
    return row

def read_tracks_config(path: str, sheet="config"):
    df = pd.read_excel(path, sheet_name=sheet)
    df.columns = df.columns.str.lower().str.strip()

    if "release_date" in df.columns:
        df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce").dt.date
    return df
