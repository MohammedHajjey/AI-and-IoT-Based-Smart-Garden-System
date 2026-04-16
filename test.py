import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
import pandas as pd
import os

# Veri seti yolu
data_path = "data"

# Veriyi yükleme
images = []
labels = []

for subfolder in os.listdir(data_path):
    subfolder_path = os.path.join(data_path, subfolder)
    if not os.path.isdir(subfolder_path):
        continue

    for image_filename in os.listdir(subfolder_path):
        image_path = os.path.join(subfolder_path, image_filename)
        images.append(image_path)
        labels.append(subfolder)

data = pd.DataFrame({'image': images, 'label': labels})

# Veri setini bölme
strat = data['label']
train_df, dummy_df = train_test_split(data, train_size=0.81, shuffle=True, random_state=123, stratify=strat)

strat = dummy_df['label']
valid_df, test_df = train_test_split(dummy_df, train_size=0.5, shuffle=True, random_state=123, stratify=strat)

# Parametreler
img_height, img_width = 128, 128  # Girdi boyutları
batch_size = 32
num_classes = len(data['label'].unique())  # Sınıf sayısı

# Veri artırma ve ön işleme
train_datagen = ImageDataGenerator(rescale=1./255,
                                    rotation_range=20,
                                    width_shift_range=0.2,
                                    height_shift_range=0.2,
                                    shear_range=0.2,
                                    zoom_range=0.2,
                                    horizontal_flip=True)
val_test_datagen = ImageDataGenerator(rescale=1./255)

def dataframe_to_generator(df, datagen, target_size, batch_size):
    return datagen.flow_from_dataframe(
        dataframe=df,
        directory=None,
        x_col="image",
        y_col="label",
        target_size=target_size,
        batch_size=batch_size,
        class_mode="categorical"
    )

train_data = dataframe_to_generator(train_df, train_datagen, (img_height, img_width), batch_size)
val_data = dataframe_to_generator(valid_df, val_test_datagen, (img_height, img_width), batch_size)
test_data = dataframe_to_generator(test_df, val_test_datagen, (img_height, img_width), batch_size)

# Model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(num_classes, activation='softmax')
])

# Modeli derleme
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy']) 

# Early stopping
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Modeli eğitme
history = model.fit(train_data,
                    validation_data=val_data,
                    epochs=30,
                    callbacks=[early_stopping])

# Modeli değerlendirme
test_loss, test_accuracy = model.evaluate(test_data)
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

# Modeli kaydetme
model.save("corn_disease_cnn_model.h5")
