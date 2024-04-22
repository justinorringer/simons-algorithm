import os
import sys
from dotenv import load_dotenv

load_dotenv()

from qiskit_ibm_runtime import QiskitRuntimeService

def get_service():
    token = os.environ.get('IBM_TOKEN')
    if token == "" or token is None:
        print("Please set the IBM_TOKEN environment variable to use quantum hardware.")
        exit(1)

    return QiskitRuntimeService(
        channel='ibm_quantum',
        instance='ibm-q/open/main',
        token=token
    )

def get_job():
    job_id = sys.argv[1] if len(sys.argv) > 1 else ""
    print("JOB ID:", job_id)
    if job_id == "":
        print("Please pass the JOB ID.")
        exit(1)

    return job_id

def get_export_path():
    export_path = sys.argv[2] if len(sys.argv) > 2 else "results/{job_id}.png"
    print("EXPORT PATH:", export_path)

    return export_path
