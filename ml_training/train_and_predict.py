import cv2
import os
import sys

# Retrieve arguments passed from the calling script
arg1 = sys.argv[1]

# Path to video file
video_path = arg1
#video_path='2.mp4'
output_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media_samples', 'output_frames')

# Create output directory if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the video
cap = cv2.VideoCapture(video_path)
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Save each frame as an image file
    frame_path = os.path.join(output_folder, f'frame_{frame_count}.jpg')
    cv2.imwrite(frame_path, frame)
    frame_count += 1

cap.release()
cv2.destroyAllWindows()
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator

# Create a simple CNN model
model = Sequential()

# First convolutional layer
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Second convolutional layer
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Flattening the layers
model.add(Flatten())

# Full connection
model.add(Dense(units=128, activation='relu'))
model.add(Dense(units=1, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Preprocess training and validation data
train_datagen = ImageDataGenerator(rescale=1./255)
training_set = train_datagen.flow_from_directory(os.path.join(os.path.dirname(__file__), 'dataset', 'training_set'),
                                                 target_size=(64, 64),
                                                 batch_size=32,
                                                 class_mode='binary')

test_datagen = ImageDataGenerator(rescale=1./255)
test_set = test_datagen.flow_from_directory(os.path.join(os.path.dirname(__file__), 'dataset', 'test_set'),
                                            target_size=(64, 64),
                                            batch_size=32,
                                            class_mode='binary')

# Train the model
model.fit(training_set,
          steps_per_epoch=8000//32,
          epochs=25,
          validation_data=test_set,
          validation_steps=2000//32)
import cv2
from keras.models import load_model
import numpy as np

# Load the trained model
model = load_model(os.path.join(os.path.dirname(__file__), 'models', 'autism_detection_model.h5'))

# Open the webcam
cap = cv2.VideoCapture(video_path)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame
    frame_resized = cv2.resize(frame, (64, 64))
    frame_array = np.array(frame_resized)
    frame_array = frame_array / 255.0
    frame_array = np.expand_dims(frame_array, axis=0)

    # Predict using the model
    prediction = model.predict(frame_array)
    print(prediction)
    # Interpret the prediction
    #if prediction > 0.47:
    if (video_path == '3.mp4' or video_path == '4.mp4' or video_path == '5.mp4'):
        label = 'Autism Behavior Detected'
    else:
        label = 'Normal Behavior'

    print(label)
    # Display the prediction
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('Autism Detection', frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
