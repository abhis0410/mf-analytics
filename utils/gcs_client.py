import json
from google.cloud import storage
from google.oauth2 import service_account
import streamlit as st
import re

class GCSClient:
    def __init__(self, bucket_name: str, file_name: str):
        self.bucket_name = bucket_name
        self.file_name = file_name

        raw_json = st.secrets["gcs"]["service_account_json"]
        fixed_json = re.sub(r'("private_key"\s*:\s*")(.+?)(")', 
                            lambda m: m.group(1) + m.group(2).replace('\n', '\\n') + m.group(3), 
                            raw_json, flags=re.DOTALL)

        service_account_info = json.loads(fixed_json)        
        credentials = service_account.Credentials.from_service_account_info(service_account_info)
        
        self.client = storage.Client(credentials=credentials, project=service_account_info["project_id"])
        self.bucket = self.client.bucket(bucket_name)

    def load_data(self):
        blob = self.bucket.blob(self.file_name)
        if blob.exists():
            return json.loads(blob.download_as_text())
        else:
            self.save_data([])
            return []

    def save_data(self, data):
        blob = self.bucket.blob(self.file_name)
        blob.upload_from_string(json.dumps(data, indent=4), content_type="application/json")
