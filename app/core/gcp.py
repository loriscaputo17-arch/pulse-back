import json
import os
import tempfile

def setup_gcp_credentials():
    """
    Write GCP credentials JSON to a temp file and
    set GOOGLE_APPLICATION_CREDENTIALS
    """
    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if not creds_json:
        return  # local dev or already configured

    creds = json.loads(creds_json)

    tmp_file = tempfile.NamedTemporaryFile(
        mode="w",
        delete=False,
        suffix=".json"
    )
    json.dump(creds, tmp_file)
    tmp_file.flush()

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = tmp_file.name
