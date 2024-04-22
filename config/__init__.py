from dotenv import load_dotenv
import os

load_dotenv()

IBM_TOKEN = os.getenv("IBM_TOKEN")
if IBM_TOKEN == "":
    print("Please set the IBM_TOKEN environment variable to use quantum hardware.")
    exit(1)

MOCK = os.getenv("MOCK", "false").lower() == "true"
if MOCK:
    print("Using mock backend.")
else:
    print("Using real backend.")

# make directory for circuits and results
if not os.path.exists("circuits"):
    os.makedirs("circuits")
if not os.path.exists("results"):
    os.makedirs("results")
