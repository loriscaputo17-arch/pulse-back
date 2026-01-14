from fastapi import APIRouter, HTTPException
from google.cloud import bigquery
from app.core.config import settings

router = APIRouter(prefix="/artists", tags=["Tracks"])

def get_table(name: str):
    return f"{settings.GCP_PROJECT}.{settings.BQ_DATASET}.{name}"

@router.get("/{artist_id}/tracks/{track_id}")
async def get_track_detail(artist_id: str, track_id: int):
    client = bigquery.Client()

    # 1️⃣ TRACK INFO
    track_job = client.query(
        f"""
        SELECT *
        FROM `{get_table("artist_song")}`
        WHERE artist_id = @artist_id
          AND song_id = @track_id
        LIMIT 1
        """,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("artist_id", "STRING", artist_id),
                bigquery.ScalarQueryParameter("track_id", "INT64", track_id),
            ]
        )
    )

    track = next(track_job.result(), None)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    # 2️⃣ DAILY METRICS
    daily_job = client.query(
        f"""
        SELECT date, streams, listeners, playlist_adds, saves
        FROM `{get_table("track_daily_metrics")}`
        WHERE artist_id=@artist_id AND track_id=@track_id
        ORDER BY date
        """,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("artist_id", "STRING", artist_id),
                bigquery.ScalarQueryParameter("track_id", "INT64", track_id),
            ]
        )
    )

    # 3️⃣ PLAYLISTS
    playlists_job = client.query(
        f"""
        SELECT playlist, creator, streams
        FROM `{get_table("song_playlists")}`
        WHERE artist_id=@artist_id AND track_id=@track_id
        ORDER BY streams DESC
        """,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("artist_id", "STRING", artist_id),
                bigquery.ScalarQueryParameter("track_id", "INT64", track_id),
            ]
        )
    )

    countries_job = client.query(
        f"""
        SELECT rank, country, streams
        FROM `{get_table("song_countries")}`
        WHERE artist_id=@artist_id AND track_id=@track_id
        ORDER BY streams DESC
        """,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("artist_id", "STRING", artist_id),
                bigquery.ScalarQueryParameter("track_id", "INT64", track_id),
            ]
        )
    )

    cities_job = client.query(
        f"""
        SELECT rank, city, country, streams
        FROM `{get_table("song_cities")}`
        WHERE artist_id=@artist_id AND track_id=@track_id
        ORDER BY streams DESC
        """,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("artist_id", "STRING", artist_id),
                bigquery.ScalarQueryParameter("track_id", "INT64", track_id),
            ]
        )
    )

    return {
        "track": dict(track),
        "daily_chart": [dict(r) for r in daily_job.result()],
        "playlists": [dict(r) for r in playlists_job.result()],
        "countries": [dict(r) for r in countries_job.result()],
        "cities": [dict(r) for r in cities_job.result()],
    }


@router.get("/{artist_id}/tracks")
async def get_artist_tracks(artist_id: str):
    client = bigquery.Client()

    job = client.query(
        f"""
        SELECT
          song_id,
          track,
          streams,
          listeners,
          playlist_adds,
          saves,
          release_date,
          image
        FROM `{get_table("artist_song")}`
        WHERE artist_id = @artist_id
        ORDER BY streams DESC
        """,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("artist_id", "STRING", artist_id)
            ]
        )
    )

    return {"tracks": [dict(r) for r in job.result()]}
