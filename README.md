# Penny Investment Manager
## Training, Validation, and Implementation

This repository provides the backbone for the Penny Investment Management code. Included is the scripts to train (hidden for you suckers), validate and test edge cases, and then implement into usage.

---

## Technical Overview & Methodology

The core architecture operates across three interconnected modules: predictive feature construction, historical portfolio simulation, and live signal dispatch.


```

+-----------------------------------------------------------------------------------+
|                           1. MODEL PREDICTIVE PIPELINE                            |
|                                                                                   |
|  Historical Market Data ---> Feature Vector Construction ---> Probabilistic Score |
+-----------------------------------------------------------------------------------+

|
v

+-----------------------------------------------------------------------------------+
|                        2. SIMULATION & BACKTESTING ENGINE                         |
|                                                                                   |
|  Signal Evaluation ---> Threshold Scaling ---> Ledger & Capital Reallocation      |
+-----------------------------------------------------------------------------------+

|
v

+-----------------------------------------------------------------------------------+
|                      3. REAL-TIME INFERENCE & ALERT SERVICE                       |
|                                                                                   |
|  Live Data Ingestion ---> Dynamic Feature Tensor ---> Alert & Diagnostic Delivery |
+-----------------------------------------------------------------------------------+

```

### 1. Feature Engineering & Predictive Modeling
* **Relative Input Transformation**: To enforce scale invariance across varying market regimes and price magnitudes, the predictive engine constructs input vectors from continuous relative percentage changes across consecutive trading intervals rather than raw nominal stock prices.
* **Class Asymmetry Handling**: Directional price movements in financial time series frequently exhibit class imbalance. The training pipeline incorporates cost-sensitive loss weighting to penalize misclassifications differentially according to strategic risk preferences (e.g., heavily penalizing false positives to preserve capital).
* **Model Regularization**: Generalization performance is enforced using dropout layers and $L_2$ weight regularization penalties to prevent overfitting to noisy historical price data.

### 2. Backtesting & Portfolio Simulation Framework
* **Dynamic Historical Windowing**: To avoid lookahead bias while maintaining feature completeness from day one of a simulation, the system automatically fetches a dynamic historical buffer window prior to the specified evaluation start date.
* **Capital Allocation & Position Execution**: The backtester maintains an active state tracking available cash, equity shares, and net portfolio valuation:
  $$\text{Portfolio Value}_t = \text{Cash}_t + (\text{Shares}_t \times P_t)$$
  * **Threshold-Based Reallocation**: Capital transitions between cash and equity assets when confidence probabilities cross user-defined upper or lower decision boundaries.
  * **Audit Trail Generation**: Daily asset valuations, active signals, executed trades, and account equity are logged to an immutable CSV ledger.

### 3. Live Inference & Mobile Alert Engine
* **Automated Data Processing**: The real-time service polls active market data via REST APIs near market close, formats dynamic feature tensors, and passes them to the pre-trained neural network.
* **Visual Diagnostics & Encrypted Transmission**: Generates localized price diagnostic charts and dispatches formatted alerts over secure pub/sub HTTP webhooks with support for end-to-end encryption (E2EE) and self-hosted instances.

---

## Quantitative Evaluation Metrics

System performance is evaluated using both statistical learning metrics and portfolio risk indicators:

### 1. Statistical Precision (Capital Protection)
$$\text{Precision} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Positives}}$$
Measures the fidelity of positive trade signals. A higher precision minimizes false buy signals, reducing capital drawdown during market downtrends.

### 2. Statistical Recall / Sensitivity (Alpha Capture)
$$\text{Recall} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Negatives}}$$
Quantifies the proportion of profitable market upward movements successfully captured by the algorithm.

---

## System Usage & Execution Workflow

### Environment Setup
Install the necessary analytical and machine learning dependencies:

```bash
pip install numpy pandas tensorflow matplotlib scikit-learn yfinance requests

```

### Deploying Live Inference Routines (Doesn't work right now)

Schedule the real-time inference engine using a cron job or background runner to perform automated evaluation and dispatch mobile notifications:

```bash
python live_notifier.py --ticker SWTSX --topic your_notification_topic

```

---

## Technical Stack

* **Language**: Python 3.9+
* **Deep Learning Framework**: TensorFlow / Keras
* **Numerical Processing & Feature Extraction**: NumPy, Pandas, Scikit-Learn
* **Visualization Engine**: Matplotlib
* **Market Data Ingestion**: Open-source financial APIs (`yfinance`)
* **Alert Delivery**: `ntfy` HTTP protocol (compatible with iOS and Android)

---

## License

Distributed under the [MIT License](https://www.google.com/search?q=LICENSE).

```

```
