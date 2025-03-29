
# 🎾 Tennis Betting Model – Full Project Overview

This project is an end-to-end pipeline that uses historical tennis data to build, train, and evaluate a machine learning model for predicting tennis match outcomes – with a view to identifying profitable betting opportunities.

The approach involves scraping detailed player statistics, cleaning and merging data, engineering predictive features, training machine learning models, and simulating various betting strategies.

---


## 📦 Project Contents

This repository is structured into a series of modular Jupyter Notebooks, each handling a distinct stage of the pipeline:

---

### 1. `1. Web Scraping.ipynb` — Scraping Historical Player Stats

The first notebook handles the full web scraping process required to build a comprehensive dataset of tennis players and their performance stats across years.

#### Key Steps:

- **Collect Player URLs**:  
  Scrapes player profile URLs from ATP ranking pages hosted on matchstat.com. Because current rankings only include active players, the script accesses archived rankings (from 2001 onwards) via the site's dropdown menus to capture both retired and active players.

- **Automated Ranking Navigation**:
  - Uses `selenium` with `undetected-chromedriver` to bypass bot detection.
  - Interacts with multiple dropdown elements dynamically rendered on the page:
    - Selects specific years and the final ranking week of each year.
    - Clicks through 'View More' buttons to ensure maximum players are retrieved (up to site-imposed caps).
    - Implements wait conditions and retry loops to stabilise the scraping process.

- **Player URL Extraction**:
  - Parses the page HTML using `BeautifulSoup` to locate profile link elements.
  - Filters out duplicates and malformed entries before writing to a CSV.

- **Scraping Player Stats**:
  - Iterates through each collected player URL.
  - For each year, extracts tables of detailed statistics including:
    - Match counts by surface and round
    - Win/loss records
    - Aces, double faults, break point conversion/defence, serve stats
  - Handles dropdown-based year selection on profile pages via Selenium.
  - Extracted data is structured into dictionaries and compiled into a year-by-player dataframe.

This results in a rich, structured player statistics dataset that spans over two decades, serving as a key input for model training.

---

### 2. `2. Process Match Data.ipynb` — Clean & Prepare Match Results

- Loads historical match data from [tennis-data.co.uk](https://www.tennis-data.co.uk/)
- Splits each match into mirrored rows (winner/loser) to enable player-vs-player modelling
- Standardises match formats and outcomes
- Adds classification labels (e.g. straight-set wins)

---

### 3. `3. Process Player Data.ipynb` — Clean & Merge Player Statistics

- Loads and cleans scraped player stats
- Normalises player names to match those in the match data
#

---

### 4. `4. Create Additional Features.ipynb` — Feature Engineering

- Merges match and player dataset
- Constructs relative features (e.g. rank differences, recent form)
- Builds context-aware metrics (e.g. surface-specific performance, opponent rank bands)
- Aggregates prior match outcomes into rolling averages/scores
- Implements year-aware filtering to prevent data leakage

---

### 5. `5. Feature Selection.ipynb` — Reduce Redundancy & Prepare Final Dataset

- Identifies and removes highly correlated features
- Fills missing data with conservative imputation methods
- Drops sparse or noisy features to improve model performance

---

### 6. `6. Model Building.ipynb` — Train Predictive Models

- Chronologically splits data into train/test periods (e.g. pre-2020 vs. 2020–22)
- Trains and tunes multiple models:
  - XGBoost
  - Random Forest (baseline)
- Evaluates performance using AUC-ROC, accuracy, and calibration
- Saves the best-performing model

---

### 7. `7. Model Evaluation.ipynb` — Simulate Betting Strategies

- Applies trained models to test data and recent matches (2023–2025)
- Tests multiple betting strategies based on model predictions and bookmaker odds
- Evaluates profit/loss and total money staked



## 💷 Betting Strategy Evaluation

A range of betting strategies are simulated using the model predictions and the bookmaker odds:

### Strategies Tested:
1. **Bookmaker Favourite Strategy**: Bet if odds < 1.90
2. **Flat Stake – All Predicted Wins**
3. **Flat Stake – Where Model Odds < Bookmaker Odds**
4. **Flat Stake – Predicted Win AND Value Edge**
5. **Inverse Strategy** – Betting against model prediction when odds suggest inefficiency

Each logs:
- Total Profit/Loss
- Total Amount Staked

---

## 🧪 Final Out-of-Sample Evaluation (2023–2025)

- Model trained and tested on data up to 2022
- Predictions generated for 2023–March 2025 data
- Betting simulation run without any tuning or retraining

### Result:
Achieved a **2.81% ROI** when betting on:
- Model-predicted wins
- Where model odds implied value over bookmaker odds

---

## 📉 Limitations & Considerations

- **Variance**: Edges are small; returns may be volatile across short periods.
- **Market Drift**: Model efficacy may decline as bookmakers adjust.
- **Data Quality**: Name mismatches or missing stats can affect reliability.
- **Real-World Frictions**: Bet limits, liquidity, and line movement reduce theoretical profits.
- **Bookmaker Odds Trustworthiness**: The Bet365 odds scraped from the historical datasets may not reflect final pre-match odds and could be subject to errors, changes, or partial recording.
- **Match Representation**: Each match was split into two mirrored rows to model each player’s win probability independently. This approach means the model can, in some cases, assign a win probability > 0.5 to both players – creating logical inconsistencies where both are predicted to win.

---

## 🔮 Next Steps

Further development and evaluation can take several paths:

### ✅ Model Evaluation

- Analyse where the model performs well (e.g. certain surfaces or tournaments).
- Investigate failure cases or consistent mismatches.
- Run statistical tests on feature importance over time.

### 🧱 Deployment & Automation

- Develop a lightweight prediction API or dashboard.
- Automate daily scraping and feature generation pipelines.
- Enable seamless integration of incoming data for real-time betting use.

### 🔄 Continuous Data Integration

- Set up pipelines to:
  - Collect new match and player data regularly.
  - Retrain or fine-tune the model periodically.
  - Store predictions in a central database for strategy testing.

### 💰 Staking Strategies

- Explore advanced staking methods:
  - **Kelly Criterion** to maximise long-term growth.
  - **Proportional Flat Staking** as a low-risk baseline.
  - Risk-adjusted Kelly to balance aggressiveness with variance.

### 📈 Model Enhancement

- Incorporate more player-level or situational features (e.g. injuries, travel/fatigue, time zones).
- Consider ensemble models or meta-models combining multiple predictors.
- Track opponent form dynamically across a tournament, not just historic averages.

### 🌍 Expansion to Other Markets & Sports

- Leverage the current pipeline structure to model other tennis betting markets (e.g. total games, set betting, break points).
- Apply the general scraping, feature engineering, and modelling methodology to other sports with structured data (e.g. football, basketball, cricket).
- Explore cross-sport generalisability of profitable betting strategies.