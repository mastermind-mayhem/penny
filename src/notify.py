import os
import requests
import matplotlib.pyplot as plt

# Define your ntfy topic name
TOPIC_NAME = "penny_stock_alerts_98432"
NTFY_URL = f"https://ntfy.sh/{TOPIC_NAME}"

def create_dummy_chart(filename="dummy_chart.png"):
    """
    Generates a dark-themed sample line chart with 6 data points.
    """
    dates = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6"]
    prices = [100.20, 101.50, 99.80, 102.10, 103.40, 105.00]

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 4), dpi=150)
    
    # Plot line and markers
    ax.plot(dates, prices, marker='o', color='#00E676', linewidth=2.5, markersize=6)
    
    # Chart styling
    ax.set_title("DEMO - Last 6 Prices (Model Confidence: 87.5%)", fontsize=11, pad=12)
    ax.set_ylabel("Price ($)", fontsize=9)
    ax.grid(True, linestyle='--', alpha=0.3)

    # Annotate price values on chart points
    for i, price in enumerate(prices):
        ax.annotate(f"${price:.2f}", (dates[i], prices[i]), 
                    textcoords="offset points", xytext=(0, 8), 
                    ha='center', fontsize=8)

    plt.tight_layout()
    plt.savefig(filename, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    return filename

def send_test_notification():
    """
    Generates chart and pushes it as an attachment via ntfy.sh
    """
    chart_filepath = create_dummy_chart()

    # Define notification metadata without emojis
    headers = {
        "Title": "BUY SIGNAL: DEMO at $105.00",
        "Priority": "high",
        "Filename": "price_trend.png"
    }

    # Define notification text
    message = (
        "Model Confidence: 87.5%\n"
        "Latest Price: $105.00\n"
        "6-Period Momentum: +4.79%\n"
        "Threshold Trigger: 0.65\n\n"
        "Status: Graph test notification successfully sent."
    )

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

if __name__ == "__main__":
    send_test_notification()