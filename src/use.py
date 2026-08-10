#region imports
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"   # 0=all, 1=info, 2=warning, 3=error only
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  # disable oneDNN messages (optional)
import configparser
import requests
import matplotlib.pyplot as plt
import yfinance as yf
import tensorflow as tf
import time, schedule
#endregion imports

@tf.keras.utils.register_keras_serializable()
def weighted_binary_crossentropy(y_true, y_pred, weight=1.0):
    epsilon = tf.keras.backend.epsilon()
    y_pred = tf.clip_by_value(y_pred, epsilon, 1.0 - epsilon)
    
    bce = - (weight * y_true * tf.math.log(y_pred) + (1 - y_true) * tf.math.log(1 - y_pred))
    return tf.reduce_mean(bce, axis=-1)

# Initialize parser
config = configparser.ConfigParser()
config.read('/opt/penny/src/config.ini')

# --- Access Single Configuration Values ---
MODEL_PATH = "./penny.keras"
LIVE_DAYS = config.getint('DATA', 'LIVE_DATA_DAYS')
raw_tickers = config.get('DATA', 'TICKERS')
TICKERS = [ticker.strip().upper() for ticker in raw_tickers.split(',') if ticker.strip()]
DECISION_THRESHOLD = config.getfloat('EXECUTION', 'DECISION_THRESHOLD')
DEFAULT_INVESTMENT = config.getfloat('EXECUTION', 'DEFAULT_INVESTMENT')
TOPIC_NAME = config.get('EXECUTION', 'URL_TOPIC_NAME')
EXEC_TIME = config.get('EXECUTION', 'ACTIVATION_TIME')
NTFY_URL = f"https://ntfy.sh/{TOPIC_NAME}"


def create_chart(predictions, closes, percents, dates, filename="chart.png"):
    """
    Generates a dark-themed sample line chart with 6 data points.
    """
    prices = closes[6:]

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 4), dpi=150)
    
    # Plot line and markers
    ax.plot(dates, prices, marker='o', color='#00E676', linewidth=2.5, markersize=6)
    
    # Chart styling
    ax.set_title("Model Confidence & Stock Variation", fontsize=11, pad=12)
    ax.set_ylabel("Price ($)", fontsize=9)
    ax.grid(True, linestyle='--', alpha=0.3)


    # Annotate price values on chart points
    for i, prediction in enumerate(predictions):
        ax.annotate(f"{prediction * 100:.2f}%", (dates[i], prices[i]), 
                    textcoords="offset points", xytext=(1, 8), 
                    ha='center', fontsize=8)
    for i, percent in enumerate(percents):
        ax.annotate(f"{percent * 100:.2f}%", (dates[i], prices[i]), 
                    textcoords="offset points", xytext=(1, -8), 
                    ha='center', fontsize=8)

    plt.tight_layout()
    plt.savefig(filename, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    return filename

def send_test_notification(predictions, closes, percents, dates, name):
    """
    Generates chart and pushes it as an attachment via ntfy.sh
    """
    chart_filepath = create_chart(predictions, closes, percents, dates)

    # Define notification metadata without emojis
    if predictions[-1] >= DECISION_THRESHOLD:
        headers = {
            "Title": f"BUY SIGNAL: {name} at ${closes[-1]:.2f}",
            "Priority": "high",
            "Filename": "price_trend.png"
        }

        # Define notification text
        message = (
            f"Model Confidence: {predictions[-1] * 100:.2f}%\n"
            f"Latest Price: {closes[-1]:.2f}\n"
            f"Threshold Trigger: {DECISION_THRESHOLD*100}%\n\n"
        )
    else:
        headers = {
            "Title": f"Update: {name} at ${closes[-1]:.2f}",
            "Priority": "low",
            "Filename": "price_trend.png"
        }

        # Define notification text
        message = (
            f"Model Confidence: {predictions[-1] * 100:.2f}%\n"
            f"Latest Price: {closes[-1]:.2f}\n"
            f"Threshold Trigger: {DECISION_THRESHOLD*100}%\n\n"
        )
    print(message)

    print(f"Sending test notification with chart to topic '{TOPIC_NAME}'...")
    
    try:
        # POST image file to ntfy endpoint with message params
        with open(chart_filepath, "rb") as image_file:
            response = requests.post(
                NTFY_URL,
                data=image_file,
                headers=headers,
                params={"message": message}
            )

        if response.status_code == 200:
            print("SUCCESS: Notification sent successfully.")
        else:
            print(f"ERROR: Failed to send notification. Status: {response.status_code} - {response.text}")

    finally:
        # Clean up local temporary file
        if os.path.exists(chart_filepath):
            os.remove(chart_filepath)

def calculate():
    print(f"Starting calculation at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    for ticker in TICKERS:
        name = ticker
        ticker = yf.Ticker(ticker)
        # Fetch historical closes_s for the last 14 days to ensure 7 trading days
        df = ticker.history(period="28d")
        timestamps = (df.index[-7:]).tolist()
        dates = [ts.strftime('%m/%d') for ts in timestamps]
        # print(f"Fetched last 7 dates for {ticker.info['symbol']}: {dates}")
        df["Close"] = df["Close"].round(2)
        closes = df["Close"].tail(13).tolist()
        print(f"Fetched last 7 closes_s for {ticker.info['symbol']}: {closes}")

        input_prices = []
        for i in range(7):
            input_prices.append(list(reversed(closes[i:i+7])))
            print(input_prices[-1])
        input_prices = list(reversed(input_prices))
        input_per = []
        percents = []
        for day in input_prices:
            xs = []
            first = True
            for i in range(len(day)-1):
                if first:
                    first = False
                    percents.append((day[i]-day[i+1])/day[i+1])
                xs.append((day[i]-day[i+1])/day[i+1])
            print(xs)
            input_per.append(xs)
        percents = list(reversed(percents))

        # Load the TensorFlow model
        model = tf.keras.models.load_model(MODEL_PATH)
        predictions = []
        for x in input_per:
            # Convert normalized list to a TensorFlow tensor
            input_data = tf.convert_to_tensor([x], dtype=tf.float32)

            # Run the model to get predictions
            predictions.append(model.predict(input_data, verbose=0).flatten()[0])

        # Print the predictions
        predictions = list(reversed(predictions))
        send_test_notification(predictions, closes, percents, dates, name)

if __name__ == "__main__":
    # Schedule Execution
    schedule.every().day.at(EXEC_TIME).do(calculate)
    print("Scheduler is running")
    while True:
        schedule.run_pending()
        time.sleep(1)