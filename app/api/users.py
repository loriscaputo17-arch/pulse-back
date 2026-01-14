from fastapi import APIRouter, HTTPException, Depends, Request
from google.cloud import bigquery
from app.core.config import settings
from app.services.supabase import get_supabase_admin

router = APIRouter()
 
def get_table(name: str):
    return f"{settings.GCP_PROJECT}.{settings.BQ_DATASET}.{name}"

@router.get("/users/{user_id}/stats")
async def get_user_stats(user_id: str):
    client = bigquery.Client()

    # 1️⃣ DAILY METRICS
    daily_query = f"""
        SELECT
          date,
          listeners,
          streams,
          followers,
          saves
        FROM `{get_table("user_daily_metrics")}`
        WHERE user_id = @user_id
        ORDER BY date
    """

    daily_job = client.query(
        daily_query,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
            ]
        )
    )

    daily_chart = [dict(row) for row in daily_job.result()]

    # 2️⃣ TOTAL SAVES
    saves_query = f"""
        SELECT total_saves
        FROM `{get_table("artist_saves")}`
        WHERE artist_id = @user_id
        LIMIT 1
    """

    saves_job = client.query(
        saves_query,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
            ]
        )
    )

    saves_row = next(saves_job.result(), None)
    total_saves = saves_row["total_saves"] if saves_row else 0

    # 3️⃣ TOP COUNTRIES
    countries_query = f"""
        SELECT
          rank,
          country AS paese,
          listeners
        FROM `{get_table("artist_countries")}`
        WHERE user_id = @user_id
        ORDER BY rank
        LIMIT 5
    """

    countries_job = client.query(
        countries_query,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
            ]
        )
    )

    top_countries = [dict(row) for row in countries_job.result()]

    return {
        "daily_chart": daily_chart,
        "total_saves": total_saves,
        "top_countries": top_countries
    }


@router.get("/users/{user_id}/daily-metrics")
async def get_user_daily_metrics(user_id: str):
    client = bigquery.Client()

    query = f"""
        SELECT *
        FROM `{get_table("user_daily_metrics")}`
        WHERE user_id = @user
        ORDER BY date
    """

    job = client.query(
        query,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("user", "STRING", user_id)
            ]
        )
    )

    df = job.to_dataframe()
    return df.to_dict("records")
