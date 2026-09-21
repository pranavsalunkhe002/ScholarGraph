import pandas as pd
from pathlib import Path


def load_dataset():
    """
    Load the ScholarGraph research paper dataset.
    """

    project_root = Path(__file__).resolve().parents[2]

    dataset_path = project_root / "data" / "raw" / "research_papers.csv"

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {dataset_path}"
        )

    df = pd.read_csv(dataset_path)

    return df


if __name__ == "__main__":
    df = load_dataset()

    print("Dataset loaded successfully!")
    print(f"Number of papers: {len(df)}")
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 records:")
    print(df.head())