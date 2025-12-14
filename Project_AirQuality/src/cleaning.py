import pandas as pd
from pathlib import Path
from data_loading import load_data

BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    - Parse Date to datetime
    - Standardize categorical text
    - Drop extremely missing columns (optional but recommended)
    - Keep NaNs (no aggressive imputation yet)
    """
    df = df.copy()

    # 1) Parse Date
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # 2) Basic text cleanup
    df["City"] = df["City"].astype(str).str.strip()
    df["AQI_Bucket"] = df["AQI_Bucket"].astype(str).str.strip()

    # 3) Drop columns with too many missing values (threshold = 60%)
    #    This keeps the dataset usable for EDA without throwing away rows.
    missing_ratio = df.isna().mean()
    cols_to_drop = missing_ratio[missing_ratio > 0.60].index.tolist()

    # Keep the list explicit in logs
    if cols_to_drop:
        print(f"Dropping columns (>60% missing): {cols_to_drop}")
        df = df.drop(columns=cols_to_drop)

    return df


def save_clean_base(df: pd.DataFrame, filename: str = "air_quality_clean_base.csv") -> Path:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROCESSED_DIR / filename
    df.to_csv(out_path, index=False)
    return out_path


def main():
    df_raw = load_data()
    df_clean = basic_clean(df_raw)

    print("\n=== After basic_clean ===")
    print(f"Shape: {df_clean.shape}")
    print("\nMissing values (top 10):")
    print(df_clean.isna().sum().sort_values(ascending=False).head(10))

    out_path = save_clean_base(df_clean)
    print(f"\nSaved clean base to: {out_path}")


if __name__ == "__main__":
    main()
