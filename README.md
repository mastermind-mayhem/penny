# Penny Investment Manager
## Training, Validation, and Implementation

This repository provides the backbone for the Penny Investment Management code. Included is the scripts to train, validate and test edge cases, and then implement into usage.

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
See full overview in [this documentation.](./OVERVIEW.md)


## System Usage & Execution Workflow


### Deploying Docker Container

Grab dockerfile and initialize container
```bash
docker build -t penny_build https://raw.githubusercontent.com/mastermind-mayhem/penny/deploy/Dockerfile
docker run --name penny -d penny_build
```

Configure `config.ini` to customize what stocks to watch and what confidence level to have:

```bash
docker exec -it penny bash
sudo apt-get update
sudo apt-get install -y nano
sudo nano /opt/penny/config.ini
```

### Installing Individually on Linux

Pull the install script from the repository
```bash
curl -O https://raw.githubusercontent.com/mastermind-mayhem/penny/deploy/install.sh
```
Recognize as a Shell Script and execute
```bash
sudo chmod +x install.sh
sudo ./install.sh
```

Configure `config.ini` to customize what stocks to watch and what confidence level to have:

```bash
sudo nano /opt/penny/config.ini
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


