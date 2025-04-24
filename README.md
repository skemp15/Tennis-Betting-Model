# 🎾 Tennis Betting Model – Full Project Overview

This project is an end-to-end pipeline that uses historical tennis data to build, train, and evaluate a machine learning model for predicting tennis match outcomes – with a view to identifying profitable betting opportunities.

The approach involves scraping detailed player statistics, cleaning and merging data, engineering predictive features, training machine learning models, and simulating various betting strategies.

---

## 📦 Project Contents

This repository is structured into a series of modular Jupyter Notebooks, each handling a distinct stage of the pipeline:

---

### 1. `1. Web Scraping.ipynb` — Scraping Historical Player Stats  
Scrapes ATP player profiles and seasonal stats (from 2001 onward) using Selenium and BeautifulSoup, overcoming site limitations with automated dropdown selection and stability controls.

---

### 2. `2. Process Match Data.ipynb` — Clean & Prepare Match Results  
Loads and standardises historical match data, splits matches into mirrored player rows for independent win probability modelling.

---

### 3. `3. Process Player Data.ipynb` — Clean & Merge Player Statistics  
Cleans scraped player-level data and aligns player names to match those in the results dataset.

---

### 4. `4. Create Additional Features.ipynb` — Feature Engineering  
Merges datasets, builds surface-aware and context-specific features, aggregates past performance into rolling metrics, and ensures no future data leaks into training.

---

### 5. `5. Feature Selection.ipynb` — Reduce Redundancy & Prepare Final Dataset  
Removes highly correlated and low-signal features, imputes missing data conservatively, and prepares the final modelling dataset.

---

### 6. `6. Model Building.ipynb` — Train Predictive Models  
Trains and evaluates multiple models (Random Forest, XGBoost), using chronologically split data. The best model is selected based on out-of-sample accuracy and calibration.

---

### 7. `7. Model Evaluation.ipynb` — Model Evaluation  
Analyses model performance across multiple dimensions, including prediction confidence, match surface, and player types. Evaluates metrics like AUC-ROC, calibration, and win probability reliability. Identifies overconfident or miscalibrated segments and highlights where the model performs strongest.

---

### 8. `8. Profit & Loss Analysis.ipynb` — Profit & Loss Analysis  
Simulates a variety of betting strategies, including flat-staking and multiple Kelly staking variations. Compares returns, volatility, and drawdowns. Highlights how different levels of risk appetite affect long-term profitability, and shows that while aggressive Kelly strategies offer high returns, they also bring greater exposure to loss and practical betting limitations.

---

## 💷 Betting Strategy Evaluation

A range of betting strategies are simulated based on model predictions and bookmaker odds.

### Strategies Tested:
1. **Bookmaker Favourite Strategy**: Bet when odds are short (<1.90)  
2. **Flat Stake – All Predicted Wins**  
3. **Flat Stake – Value-Only Bets (Model Odds < Bookmaker Odds)**  
4. **Flat Stake – Predicted Win *and* Value**  
5. **Inverse Strategy** – Betting against predicted winners when odds suggest inefficiency

Each logs:
- Total Profit/Loss
- Total Amount Staked
- ROI
- Drawdowns and volatility (via P&L curves)

---

## 🧪 Final Out-of-Sample Evaluation (2023–2025)

The model was trained on data up to 2022 and evaluated out-of-sample on unseen matches from 2023 to early 2025.

### Result:  
Achieved a **4.78% ROI** using flat-stake bets on:
- Model-predicted winners
- Where the model saw value against bookmaker odds

---

## 📉 Limitations & Considerations

- **Variance**: Short-term results may be volatile due to small average edge.  
- **Market Drift**: As odds providers adjust, model performance may erode.  
- **Real-World Frictions**: Includes bet size limits, liquidity, and delays.  
- **Bookmaker Odds**: Historical odds may differ from final closing prices.  
- **Model Conflicts**: Mirrored match representation can cause logical issues in some matchups.

---

## 🔮 Next Steps

### 🧱 Automation & Deployment
- Build a prediction dashboard or lightweight API
- Automate scraping and model updates for real-time use

### ♻️ Continuous Updates
- Retrain regularly with new match data
- Dynamically update performance tracking

### 🌍 Cross-Sport Expansion
- Adapt methodology for football, basketball, or other structured sports markets
