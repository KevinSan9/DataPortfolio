import pandas as pd
from data_loading import load_data

def main():
    df =  load_data()
    print("\n=== Dataset shape ===")
    print(df.shape)
    print("\n=== Column names ===")
    print(df.columns)
    print("\n=== Data types ===")
    print(df.dtypes)
    print("\n=== Missing values (top 15) ===")
    print(df.isnull().sum().sort_values(ascending=False).head(15))
    print("\n=== First 5 rows ===")
    print(df.head())

if __name__=="__main__":
    main()