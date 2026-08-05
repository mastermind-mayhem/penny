import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"   # 0=all, 1=info, 2=warning, 3=error only
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  # disable oneDNN messages (optional)

import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

@tf.keras.utils.register_keras_serializable()
def weighted_binary_crossentropy(y_true, y_pred, weight=1.0):
    epsilon = tf.keras.backend.epsilon()
    y_pred = tf.clip_by_value(y_pred, epsilon, 1.0 - epsilon)
    
    bce = - (weight * y_true * tf.math.log(y_pred) + (1 - y_true) * tf.math.log(1 - y_pred))
    return tf.reduce_mean(bce, axis=-1)

# Load the trained model
model = tf.keras.models.load_model('penny.keras')
# Load dataset from test.csv
# Column 1 (idx 0): Stock Price
# Columns 2-7 (idx 1:7): Model Inputs
# Column 8 (idx 7): Model Outputs / Actual Label
df = pd.read_csv('data/test.csv', header=None)
print(f"✅ Loaded test dataset with shape: {df.shape}")
# Invert the rows in the CSV file
df = df.iloc[::-1].reset_index(drop=True)

# Extract inputs (Columns 2-7) and actual outputs (Column 8)
X_test = df.iloc[:, 1:7].to_numpy()
y_actual = df.iloc[:, 7].to_numpy()

# Run batch predictions
cutoff = 0.65
raw_predictions = model.predict(X_test, verbose=0).flatten()
# Scale predictions to range [0, 1]
if raw_predictions.max() != raw_predictions.min():
    predictions = (raw_predictions - raw_predictions.min()) / (raw_predictions.max() - raw_predictions.min())
else:
    predictions = np.zeros_like(raw_predictions)
print(predictions)
pred_labels = (predictions > cutoff).astype(float).flatten()
# Create a DataFrame with stock prices and predictions
output_df = pd.DataFrame({
    'Price': df.iloc[:, 0],
    'Prediction': predictions.flatten()
})


# Export stock prices and predictions to a CSV file
output_df.to_csv('data/predictions_output.csv', index=False)
print("✅ Predictions exported to 'predictions_output.csv'")
# Add a column for the stock price related to the prediction
output_df['StockPrice'] = df.iloc[:, 0]


# Calculate statistics
total = len(y_actual)
tp = np.sum((pred_labels == 1) & (y_actual == 1))
tn = np.sum((pred_labels == 0) & (y_actual == 0))
c = np.sum(pred_labels == y_actual)
fp = np.sum((pred_labels == 1) & (y_actual == 0))
fn = np.sum((pred_labels == 0) & (y_actual == 1))

print(f"Correct predictions: {c / total:.2%}")
print(f"False positives: {fp / total:.2%}")
print(f"False negatives: {fn / total:.2%}")
print(f"Precision: {tp / (tp+fp):.2%}")
print(f"Recall: {tp / (tp+fn):.2%}")

# Graph the first column (stock price) with true/false positive/negative colored line segments
stock_prices = df.iloc[:, 0].to_numpy()



#region Graphing
indices = np.arange(len(stock_prices))

# Plot stock prices by index, color-coded by actual and predicted labels
# Arrange the three plots: two on the first row, one spanning the second row
fig = plt.figure(figsize=(12, 8))
gs = fig.add_gridspec(2, 2)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, :])
# Subplot 1: Actual labels as a line plot
for i in range(len(indices) - 1):
    color = 'grey'
    ax1.plot(indices[i:i+2], stock_prices[i:i+2], color=color, linewidth=1.5)
scatter1 = ax1.scatter(indices, stock_prices, c=y_actual, cmap='spring', edgecolor='k')
cbar1 = plt.colorbar(scatter1, ax=ax1, ticks=[0, 1], label='Actual Label')
scatter1.set_clim(0, 1)
ax1.set_xlabel('Index')
ax1.set_ylabel('Stock Price')
ax1.set_title('Actual Label')
ax1.grid(True)

# Subplot 2: Predicted labels as a line plot
for i in range(len(indices) - 1):
    color = 'grey'
    ax2.plot(indices[i:i+2], stock_prices[i:i+2], color=color, linewidth=1.5)
scatter2 = ax2.scatter(indices, stock_prices, c=pred_labels, cmap='spring', edgecolor='k')
cbar2 = plt.colorbar(scatter2, ax=ax2, ticks=[0, 1], label='Predicted Label')
scatter2.set_clim(0, 1)
ax2.set_xlabel('Index')
ax2.set_ylabel('Stock Price')
ax2.set_title('Model Prediction')
ax2.grid(True)

# Subplot 3: Predictions as a line plot with gradient color
for i in range(len(indices) - 1):
    color = plt.cm.spring(predictions[i])
    ax3.plot(indices[i:i+2], stock_prices[i:i+2], color=color, linewidth=1.5)
scatter3 = ax3.scatter(indices, stock_prices, c=predictions, cmap='spring', edgecolor='k')
cbar3 = plt.colorbar(scatter3, ax=ax3, ticks=[0, 1], label='Predicted Label Duplicate')
scatter3.set_clim(0, 1)
ax3.set_xlabel('Index')
ax3.set_ylabel('Stock Price')
ax3.set_title('Model Severity Predictions')
ax3.grid(True)

plt.tight_layout()
plt.show()

#endregion Graphing
