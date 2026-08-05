import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"   # 0=all, 1=info, 2=warning, 3=error only
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  # disable oneDNN messages (optional)

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import keras

# Enable TensorFlow-DirectML plugin for GPU acceleration
# Check what's available
gpus = tf.config.list_physical_devices('GPU')

if gpus:
    try:
        # Avoid TF grabbing all GPU memory at once
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"✅ GPU available: {[gpu.name for gpu in gpus]}")
    except RuntimeError as e:
        # Memory growth must be set before GPUs are initialized
        print(e)
else:
    print("⚠️ No GPU found — running on CPU")

# Load pre-scaled/normalized data from local CSV (no header assumed, slice first 7 columns)
df = pd.read_csv('data/train.csv', header=None)

# Extract features (first 6 columns: indices 0 to 5) and target (7th column: index 6)
X = df.iloc[:, 0:6].to_numpy()
y = df.iloc[:, 6].to_numpy()

# Train/Test Splits
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Sub-splits for evaluation
mid = len(X_test) // 2
X_test1, X_test2 = X_test[:mid], X_test[mid:]
y_test1, y_test2 = y_test[:mid], y_test[mid:]

# Build Neural Network
model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation='relu', input_shape=(X.shape[1],)),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(4, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(16, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    tf.keras.layers.Dense(1, activation='sigmoid')
])


@tf.keras.utils.register_keras_serializable()
def weighted_binary_crossentropy(y_true, y_pred, weight=1.0):
    epsilon = tf.keras.backend.epsilon()
    y_pred = tf.clip_by_value(y_pred, epsilon, 1.0 - epsilon)
    
    bce = - (weight * y_true * tf.math.log(y_pred) + (1 - y_true) * tf.math.log(1 - y_pred))
    return tf.reduce_mean(bce, axis=-1)


# Find optimal class weights
# class_weights = {0: weights[0], 1: weights[1]}
class_weights = {0: 2.5, 1: 1.0}

print("Automated Square Root Weights:", class_weights)

# Compile Model
model.compile(
    optimizer='adam',
    loss=weighted_binary_crossentropy,
    metrics=['accuracy']
)

# Callbacks
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=200,
    restore_best_weights=True
)

# class_weights = {0: 1.5, 1: 1.0}

# Train Model
history = model.fit(
    X_train, y_train,
    epochs=1000,
    batch_size=1024,
    validation_split=0.2,
    verbose=1,
    callbacks=[early_stop],
    class_weight=class_weights
)

print("Training stopped at epoch:", len(history.history['accuracy']))

# Evaluate Model
loss, accuracy = model.evaluate(X_test, y_test)
loss1, accuracy1 = model.evaluate(X_test1, y_test1)
print(f"Test accuracy: {accuracy:.2%}")
print(f"Test1 accuracy: {accuracy1:.2%}")

# Predict on test set
preds = model.predict(X_test)
pred_labels = (preds > 0.5).astype(int)

# Plot accuracy and loss
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='train accuracy')
plt.plot(history.history['val_accuracy'], label='val accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend()

plt.show()

# Save Model Option
if input("Do you want to save the model? (y/n): ").lower() == 'y':
    model.save('penny.keras')
    print("Model saved as 'penny.keras'")