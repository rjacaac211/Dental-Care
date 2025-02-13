import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt

# Set seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# Create results directory if not exists
results_dir = './results'
os.makedirs(results_dir, exist_ok=True)

# Load preprocessed data
X_train = np.load('X_train.npy')
X_val = np.load('X_val.npy')
y_train = np.load('y_train.npy')
y_val = np.load('y_val.npy')

print("Loaded preprocessed data:")
print("X_train shape:", X_train.shape)
print("X_val shape:", X_val.shape)
print("y_train shape:", y_train.shape)
print("y_val shape:", y_val.shape)

# Normalize pixel values
X_train = X_train.astype('float32') / 255.0
X_val = X_val.astype('float32') / 255.0

NUM_CATEGORIES = len(np.unique(y_train))
IMG_HEIGHT, IMG_WIDTH, channels = X_train.shape[1], X_train.shape[2], X_train.shape[3]

# One-hot encode labels
y_train = to_categorical(y_train, NUM_CATEGORIES)
y_val = to_categorical(y_val, NUM_CATEGORIES)

# Data augmentation
aug = ImageDataGenerator(
    rotation_range=5,
    zoom_range=0.1,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True
)

# Use MobileNetV2 for transfer learning
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(IMG_HEIGHT, IMG_WIDTH, channels))

# Freeze base model layers
for layer in base_model.layers:
    layer.trainable = False

# Add custom classification layers
x = base_model.output
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.5)(x)
x = layers.Dense(128, activation='relu')(x)
x = layers.BatchNormalization()(x)
x = layers.Dropout(0.5)(x)
predictions = layers.Dense(NUM_CATEGORIES, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model
lr = 0.001
opt = Adam(learning_rate=lr)
model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

model.summary()

# Callbacks
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True, verbose=1)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=3, verbose=1)

# Train the model
history = model.fit(
    aug.flow(X_train, y_train, batch_size=16),
    epochs=30,
    validation_data=(X_val, y_val),
    callbacks=[early_stop, reduce_lr]
)

# Evaluate the model on validation data
val_loss, val_accuracy = model.evaluate(X_val, y_val, verbose=0)
print("Validation Accuracy:", val_accuracy)
print("Validation Loss:", val_loss)

# Save the model in SavedModel format
tf.saved_model.save(model, "../models/oral_disease_saved_model")
print("Model saved in SavedModel format.")

# Save the model in .h5 format
model.save("../models/oral_disease_model.h5")
print("Model saved in HDF5 format as oral_disease_model.h5")

# Save training history as CSV
history_df = pd.DataFrame(history.history)
history_csv_path = os.path.join(results_dir, 'training_history.csv')
history_df.to_csv(history_csv_path, index=False)
print("Training history saved as training_history.csv")

# Plot training history and save the graphs
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.plot(history_df.index, history_df['accuracy'], label='Training Accuracy', linewidth=2)
ax1.plot(history_df.index, history_df['val_accuracy'], label='Validation Accuracy', linewidth=2)
ax1.set_title('Accuracy', fontsize=14)
ax1.set_xlabel('Epochs', fontsize=12)
ax1.set_ylabel('Accuracy', fontsize=12)
ax1.grid(True)
ax1.legend(fontsize=12)

ax2.plot(history_df.index, history_df['loss'], label='Training Loss', linewidth=2)
ax2.plot(history_df.index, history_df['val_loss'], label='Validation Loss', linewidth=2)
ax2.set_title('Loss', fontsize=14)
ax2.set_xlabel('Epochs', fontsize=12)
ax2.set_ylabel('Loss', fontsize=12)
ax2.grid(True)
ax2.legend(fontsize=12)

plt.tight_layout()
training_plot_path = os.path.join(results_dir, 'training_history.png')
plt.savefig(training_plot_path)
print(f"Training graphs saved to {training_plot_path}")
plt.show()
