from fastapi import APIRouter
from google.cloud import bigquery
from app.core.config import settings

router = APIRouter(prefix="/search", tags=["Search"])

def get_table(name: str):
    return f"{settings.GCP_PROJECT}.{settings.BQ_DATASET}.{name}"

@router.get("")
async def search_tracks(q: str, artist_id: str):
    client = bigquery.Client()

    query = f"""
      SELECT
        song_id,
        track,
        streams,
        listeners,
        image
      FROM `{get_table("artist_song")}`
      WHERE artist_id = @artist_id
        AND LOWER(track) LIKE LOWER(CONCAT('%', @q, '%'))
      ORDER BY streams DESC
      LIMIT 20
    """

    job = client.query(
        query,
        bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("artist_id", "STRING", artist_id),
                bigquery.ScalarQueryParameter("q", "STRING", q),
            ]
        )
    )

    return {
        "results": [dict(r) for r in job.result()]
    }
