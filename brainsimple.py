import numpy as np
from tensorflow import keras
from tensorflow.keras.layers import Dense

# --- Data (AND gate) ---
# Input (x1, x2), Output (y)
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([0, 0, 0, 1])  # AND gate truth table

# --- Model ---
model = keras.Sequential([
    Dense(1, input_shape=(2,), activation='sigmoid')  # Single neuron, sigmoid activation
])

# --- Compile ---
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# --- Train ---
model.fit(X, y, epochs=1000, verbose=0)  # Train for 1000 epochs, quiet output

# --- Test ---
predictions = model.predict(X)
print("Predictions (raw):", predictions)
rounded_predictions = np.round(predictions)
print("Predictions (rounded):", rounded_predictions)

# Get the weights and bias
weights, biases = model.layers[0].get_weights()
print("Weights:", weights)
print("Bias:", biases)
