import os
from src.county_data_collectors.county_mapper import DATA_COLLECTOR_MAP

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIRECTORY = os.path.join(ROOT, "data")
INTAKE_LABELS = os.path.join(DATA_DIRECTORY, "intake_labels.txt")
PARCEL_DATA_MAP = DATA_COLLECTOR_MAP
PARCEL_DATA_COUNTIES = list(PARCEL_DATA_MAP.keys())
