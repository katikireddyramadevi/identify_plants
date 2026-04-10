import os
import keras
from pathlib import Path

BASE_DIR = Path(r'c:\Users\Surya teja\rama\identify_plants')

@keras.saving.register_keras_serializable()
class MyDense(keras.layers.Dense):
    def __init__(self, *args, **kwargs):
        # Strip the problematic argument
        kwargs.pop('quantization_config', None)
        super().__init__(*args, **kwargs)

def test_load():
    model_path = BASE_DIR / 'models' / 'herb_leaf_model.h5'
    try:
        # We need to tell Keras to use MyDense instead of the default Dense during deserialization
        model = keras.models.load_model(str(model_path), custom_objects={'Dense': MyDense})
        print("Model loaded successfully with Custom Dense!")
        print(f"Model input shape: {model.input_shape}")
        print(f"Model output shape: {model.output_shape}")
    except Exception as e:
        print(f"Failed to load model with Custom Dense: {e}")

if __name__ == "__main__":
    test_load()
