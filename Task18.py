# CNN TASK - 18  X-RAY IMAGE CLASSIFICATION

import os    # for the dir pathing 
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator  # for data generation
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt

# pathing to dataset which is extracted 
base_dir = r"C:\Users\galli\Downloads\archive\chest_xray"
train_dir = os.path.join(base_dir,'train')
val_dir = os.path.join(base_dir, 'val')
test_dir = os.path.join(base_dir, 'test')

# data generators
train_datagen = ImageDataGenerator(rescale=1./255, zoom_range=0.2, horizontal_flip=True)
val_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_data = train_datagen.flow_from_directory(
    train_dir, target_size=(150, 150), batch_size=32, class_mode='binary')

val_data = val_datagen.flow_from_directory(
    val_dir, target_size=(150, 150), batch_size=32, class_mode='binary')

test_data = test_datagen.flow_from_directory(
    test_dir, target_size=(150, 150), batch_size=32, class_mode='binary')

# Building a CNN model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    layers.MaxPooling2D(2, 2),

    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),

    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),

    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(1, activation='sigmoid')  # binary classification
])

# Compile
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

early_stopping = EarlyStopping(monitor='val_loss', patience=3, verbose=1, mode='min', restore_best_weights= True
)

# Train the model
history = model.fit(train_data, epochs=10, validation_data=val_data, callbacks = [early_stopping]
)

# Evaluate
test_loss, test_acc = model.evaluate(test_data)
print("Test Accuracy:", test_acc)

# Save the model
model.save("pneumonia_cnn_model.keras")