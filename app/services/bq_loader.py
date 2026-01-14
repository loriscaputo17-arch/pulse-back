from google.cloud import bigquery
import pandas as pd

def load_df_to_bq(df: pd.DataFrame, table_id: str, mode="WRITE_APPEND"):
    client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(
        write_disposition=mode
    )

    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()

    return {"table": table_id, "rows": len(df)}
