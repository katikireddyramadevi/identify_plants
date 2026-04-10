import os
import keras
from pathlib import Path

BASE_DIR = Path(r'c:\Users\Surya teja\rama\identify_plants')

def test_load():
    model_path = BASE_DIR / 'models' / 'herb_leaf_model.h5'
    try:
        model = keras.models.load_model(str(model_path))
        print("Model loaded successfully with standalone keras!")
        print(f"Model input shape: {model.input_shape}")
    except Exception as e:
        print(f"Failed to load model with standalone keras: {e}")

if __name__ == "__main__":
    test_load()
