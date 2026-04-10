import os
import tensorflow as tf
import json
from pathlib import Path

BASE_DIR = Path(r'c:\Users\Surya teja\rama\identify_plants')

def test_load():
    model_path = BASE_DIR / 'medicinal_model.h5'
    print(f"Checking model path: {model_path}")
    if not model_path.exists():
        print("Model file does not exist!")
        return

    try:
        model = tf.keras.models.load_model(str(model_path))
        print("Model loaded successfully!")
        print(f"Model input shape: {model.input_shape}")
    except Exception as e:
        print(f"Failed to load model: {e}")

if __name__ == "__main__":
    test_load()
