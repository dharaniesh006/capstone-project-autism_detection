import os
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Base directory setup
BASE_DIR = os.path.dirname(__file__)

def create_model():
    # Load MobileNetV2 as the base model, excluding the top dense layers
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    # Freeze the base model to prevent weights from being updated during early training
    base_model.trainable = False
    
    # Add custom layers on top
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(1, activation='sigmoid')(x)
    
    # Combine the base model and custom top layers
    model = Model(inputs=base_model.input, outputs=predictions)
    
    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    return model

model = create_model()

# Advanced Data Augmentation to combat overfitting on small datasets
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# No augmentation for testing, just rescaling
test_datagen = ImageDataGenerator(rescale=1./255)

# Load data from directories
train_dir = os.path.join(BASE_DIR, 'dataset', 'training_set')
test_dir = os.path.join(BASE_DIR, 'dataset', 'test_set')

# Small batch size due to the limited number of samples
BATCH_SIZE = 16

training_set = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

test_set = test_datagen.flow_from_directory(
    test_dir,
    target_size=(224, 224),
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

# Callbacks to save the best model and stop early if it stops improving
model_save_path = os.path.join(BASE_DIR, 'models', 'autism_detection_model.h5')

callbacks = [
    EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True),
    ModelCheckpoint(model_save_path, monitor='val_accuracy', save_best_only=True, mode='max')
]

train_steps = max(1, training_set.samples // BATCH_SIZE)
val_steps = max(1, test_set.samples // BATCH_SIZE)

print("Starting training to achieve > 92% confidence score...")

# Train the model
model.fit(
    training_set,
    steps_per_epoch=train_steps,
    epochs=15, # 15 epochs with MobileNet is usually plenty to hit high accuracy here
    callbacks=callbacks,
    validation_data=test_set,
    validation_steps=val_steps
)

print(f"Training completed. Best model saved to: {model_save_path}")
