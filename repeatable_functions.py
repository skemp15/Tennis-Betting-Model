### Module containing all functions that may be used across different notebooks

import pandas as pd

def show_columns_with_most_nulls(df, top_n=10):
    """
    Displays the columns with the most null values in a DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame to analyse.
    - top_n (int, optional): The number of columns to display (default is 10).

    Returns:
    - null_counts (pd.DataFrame): A DataFrame containing the top columns with the most null values.

    Notes:
    - Calculates the number and percentage of null values for each column.
    - Sorts columns in descending order based on the number of missing values.
    - Prints the results and returns a DataFrame with the top columns.
    """

    # Count null values for each column
    null_counts = df.isnull().sum()

    # Compute percentage of missing values
    null_percent = (null_counts / len(df)) * 100

    # Create a DataFrame with the results
    null_summary = pd.DataFrame({
        'Null Count': null_counts,
        'Null Percentage': null_percent
    })

    # Sort by the highest null count
    null_summary = null_summary.sort_values(by='Null Count', ascending=False)

    # Display only the top_n columns with the most nulls
    top_nulls = null_summary.head(top_n)

    # Print the results
    print(f"\nTop {top_n} columns with the most null values:\n")

    return top_nulls
