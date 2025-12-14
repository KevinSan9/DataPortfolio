import pandas as pd
from pathlib import Path

# Ruta base del proyecto (Project_AirQuality)
BASE_DIR = Path(__file__).resolve().parents[1]

# Carpeta donde está el CSV
DATA_DIR = BASE_DIR / "data"

def load_data(filename: str = "dataset_original.csv") -> pd.DataFrame:
    """
    Load raw air quality dataset from data/ directory.
    """
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found at {file_path}")

    df = pd.read_csv(file_path)
    return df


if __name__ == "__main__":
    df = load_data()

    print("Dataset loaded successfully.")
    print(f"Shape: {df.shape}")
    print("\nColumns:")
    print(df.columns)

    print("\nFirst 5 rows:")
    print(df.head())
