import pandas as pd

def load_gifts(file_path):
    """
    Loads gift data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing gift data.
    """
    df = pd.read_csv(file_path)
    return df
