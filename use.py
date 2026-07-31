import yfinance as yf
import tensorflow as tf

@tf.keras.utils.register_keras_serializable()
def weighted_binary_crossentropy(y_true, y_pred, weight=1.0):
    epsilon = tf.keras.backend.epsilon()
    y_pred = tf.clip_by_value(y_pred, epsilon, 1.0 - epsilon)
    
    bce = - (weight * y_true * tf.math.log(y_pred) + (1 - y_true) * tf.math.log(1 - y_pred))
    return tf.reduce_mean(bce, axis=-1)

ticker = yf.Ticker("swtsx")

# Fetch historical closes_s for the last 14 days to ensure 7 trading days
df = ticker.history(period="14d")
closes = df["Close"].tail(7).tolist()
closes_s = []
for i in range(len(closes)-1):
    closes_s.append((closes[i]-closes[i+1])/closes[i+1])

# Load the TensorFlow model
model = tf.keras.models.load_model('penny.keras')

# Convert normalized list to a TensorFlow tensor
input_data = tf.convert_to_tensor([closes_s], dtype=tf.float32)

# Run the model to get predictions
predictions = model.predict(input_data)

# Print the predictions
print(predictions)