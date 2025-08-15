import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "raw_data"

loaders = [
    ("load_ndc", "drug-ndc-0001-of-0001.json"),
    ("load_recalls", "drug-enforcement-0001-of-0001.json"),
    ("load_shortages", "drug-shortages-0001-of-0001.json"),
    ("load_adverse_events", "drug-event-0001-of-0031.json")
]

for loader, json_file in loaders:
    json_path = DATA_DIR / json_file
    print(f"\nRunning {loader} on {json_path}...")
    try:
        subprocess.run(
            [sys.executable, "-m", f"drug_data_pipeline.loaders.{loader}", str(json_path)],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Failed to run {loader}: {e}")
