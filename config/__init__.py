import random
import sys
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

N_BITS = os.getenv("N_BITS", 5)
SIMON_SECRET = os.getenv("SIMON_SECRET", "01110")

# if random arg passed
if sys.argv[1]:
    SIMON_SECRET = str(bin(random.randint(0, 2**N_BITS - 1))).zfill(N_BITS)[2:]

# make directory for circuits and results
if not os.path.exists("circuits"):
    os.makedirs("circuits")
if not os.path.exists("results"):
    os.makedirs("results")
