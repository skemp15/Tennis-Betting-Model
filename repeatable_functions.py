### Module containing all functions that may be used across different notebooks

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import pickle

# %% --------------------------------------------------------------------------
# Show columns with most null values
# -----------------------------------------------------------------------------

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

# %% --------------------------------------------------------------------------
# Add predictions and probabilities to DataFrame
# -----------------------------------------------------------------------------

def add_preds_probs(odds_win_df, X_test, model):
    """
    Adds model predictions and converted probabilities to the odds DataFrame.

    This function:
    - Uses the provided model to predict win probabilities and outcomes on the test set.
    - Converts the predicted probabilities into an odds-style format (1/probability of outcome).
    - Appends both the predicted class and model-derived odds to the given `odds_win_df`.

    Parameters:
        odds_win_df (pandas.DataFrame): A DataFrame containing odds and outcome data for test matches.
        X_test (pandas.DataFrame): The feature set used for testing.
        model (fitted model): A trained classification model with `predict` and `predict_proba` methods.

    Returns:
        pandas.DataFrame: The input DataFrame updated with two new columns:
                          - 'model_odds': Model-derived odds based on predicted win probabilities.
                          - 'pred_win': Predicted binary outcome (win/loss).
    """
    # Make predictions on the test data
    y_pred = model.predict(X_test)

    # Get probabilities
    y_prob = model.predict_proba(X_test)

    # Convert probabilities to odds format
    y_odds = 1 / y_prob

    # Get only probability of a win
    y_prob = [prob[1] for prob in y_prob]
    y_odd = [odd[1] for odd in y_odds]

    # Add to odds_win_df
    odds_win_df['model_prob'] = y_prob
    odds_win_df['model_odds'] = y_odd
    odds_win_df['pred_win'] = y_pred

    return odds_win_df

# %% --------------------------------------------------------------------------
# Save best performing model
# -----------------------------------------------------------------------------
def save_best_model(results_df, X_train, y_train, model_name, output_path=None):
    """
    Selects the best-performing model of the specified type from the results DataFrame,
    refits it on the full training data, and saves it to a file.

    This function:
    - Filters the results to include only the specified model type.
    - Selects the configuration with the highest ROC-AUC score.
    - Instantiates the model with its best parameters and fits it to the full training data.
    - Saves the fitted model as a pickle file.

    Parameters:
        results_df (pandas.DataFrame): A DataFrame containing model names, best parameters,
                                       and evaluation metrics (e.g. 'ROC-AUC').
        X_train (pandas.DataFrame): The training features.
        y_train (pandas.Series): The training labels.
        model_name (str): The name of the model type to extract (e.g. "XGBoost", "RandomForest").
        output_path (str, optional): Path to save the trained model. If not provided,
                                     a default name is used based on the model type.

    Returns:
        str: The file path to which the model was saved.
    """

    # Validate model mapping
    model_mapping = {
        "RandomForest": RandomForestClassifier,
        "XGBoost": xgb.XGBClassifier,
    }

    # Filter for the specified model and select the best one by AUC
    filtered = results_df[results_df["Model"] == model_name]
    if filtered.empty:
        raise ValueError(f"No entries found in results_df for model type: '{model_name}'")

    best_row = filtered.sort_values(by="ROC-AUC", ascending=False).iloc[0]
    best_params = best_row["Best Params"]

    # Instantiate and fit the model
    model_class = model_mapping[model_name]
    model = model_class(**best_params)
    model.fit(X_train, y_train)

    # Determine default output path if none provided
    if output_path is None:
        output_path = f"best_{model_name.lower()}_model.pkl"

    # Save model to file
    with open(output_path, "wb") as file:
        pickle.dump(model, file)

    print(f"Saved best '{model_name}' model with ROC-AUC {best_row['ROC-AUC']:.4f} to '{output_path}'")

    return model
