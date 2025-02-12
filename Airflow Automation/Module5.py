import os
import json
from airflow.hooks.base import BaseHook

def create_file(k):
    
    conn = BaseHook.get_connection("fs_default")
    extra = conn.extra or "{}"
    file_path = json.loads(extra).get("path", "/opt/airflow/dags/run/").strip('"')
    
    os.makedirs(file_path, exist_ok=True)
    
    file_name = "status.txt"
    full_path = os.path.join(file_path, file_name)
    
    with open(full_path, "w") as f:
        f.write(str(k))
    
    print(f"File created at: {full_path}")
    
    return full_path