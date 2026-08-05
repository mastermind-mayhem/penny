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

## System Usage & Execution Workflow

### Environment Setup
Install the necessary analytical and machine learning dependencies:

```bash
pip install -r requirements.txt
```

### Deploying Live Inference Routines (Doesn't work right now)

Schedule the real-time inference engine using a cron job or background runner to perform automated evaluation and dispatch mobile notifications:

```bash
{Run Python command here}
```

## Technical Stack

* **Language**: Python 3.9+
* **Deep Learning Framework**: TensorFlow / Keras
* **Numerical Processing & Feature Extraction**: NumPy, Pandas, Scikit-Learn
* **Visualization Engine**: Matplotlib
* **Market Data Ingestion**: Open-source financial APIs 
* **Alert Delivery**: `ntfy` HTTP protocol (compatible with iOS and Android)

---

## License

Distributed under the [MIT License](https://www.google.com/search?q=LICENSE).


