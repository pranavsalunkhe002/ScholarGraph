from pathlib import Path
import sys
import pandas as pd


# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


def test_entity_extraction_output_exists():

    output_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "entities.csv"
    )

    assert output_path.exists(), (
        "Entity extraction output file was not found."
    )


def test_entity_extraction_output_not_empty():

    output_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "entities.csv"
    )

    df = pd.read_csv(output_path)

    assert len(df) > 0, (
        "Entity extraction output is empty."
    )


def test_required_entity_columns():

    output_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "entities.csv"
    )

    df = pd.read_csv(output_path)

    required_columns = {
        "entity",
        "entity_type"
    }

    assert required_columns.issubset(
        set(df.columns)
    ), (
        "Required entity columns are missing."
    )