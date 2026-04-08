import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
import numpy as np
import cv2
import os

# Constants
IMAGE_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 10


# Load your dataset
def load_data(image_dir):
    images = []
    labels = []
    for label in os.listdir(image_dir):
        for image_file in os.listdir(os.path.join(image_dir, label)):
            image_path = os.path.join(image_dir, label, image_file)
            image = cv2.imread(image_path)
            image = cv2.resize(image, IMAGE_SIZE)
            images.append(image)
            labels.append(label)

    images = np.array(images)
    labels = np.array(labels)

    return images, labels


# Preprocess the data
def preprocess_data(images, labels):
    images = images / 255.0  # Normalize pixel values to [0, 1]
    labels = np.array([0 if label == 'non_autism' else 1 for label in labels])  # Binary labels

    return train_test_split(images, labels, test_size=0.2, random_state=42)


# Build the CNN model
def create_model():
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model


# Train the model
def train_model(model, X_train, y_train, X_val, y_val):
    history = model.fit(X_train, y_train, epochs=EPOCHS,
                        validation_data=(X_val, y_val),
                        batch_size=BATCH_SIZE)
    return history


# Main function
def main():
    image_dir = 'path_to_your_dataset'  # Replace with your dataset path
    images, labels = load_data(image_dir)
    X_train, X_val, y_train, y_val = preprocess_data(images, labels)

    model = create_model()
    history = train_model(model, X_train, y_train, X_val, y_val)

    # Save the model
    model.save(os.path.join(os.path.dirname(__file__), 'models', 'autism_detection_cnn_model.h5'))


if __name__ == '__main__':
    main()
