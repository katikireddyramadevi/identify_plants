import os
import keras
from django.conf import settings

# --- CUSTOM LAYER PATCH FOR KERAS 3 COMPATIBILITY ---
@keras.saving.register_keras_serializable()
class FixDense(keras.layers.Dense):
    """
    Custom Dense layer that removes 'quantization_config' from its 
    configuration to avoid errors when loading models saved with 
    incompatible Keras versions.
    """
    def __init__(self, *args, **kwargs):
        kwargs.pop('quantization_config', None)
        super().__init__(*args, **kwargs)

_model = None

def get_model():
    """
    Singleton pattern to load and cache the TensorFlow model.
    Uses custom_objects to bypass quantization_config errors.
    """
    global _model
    if _model is None:
        model_path = os.path.join(settings.BASE_DIR, 'models', 'herb_leaf_model.h5')
        print(f"--- INITIALIZING ML MODEL (Process: {os.getpid()}) ---")
        
        if not os.path.exists(model_path):
            print(f"ERROR: Model file not found at {model_path}")
            return None
        
        try:
            # Use standalone keras and custom_objects for better compatibility
            _model = keras.models.load_model(
                model_path, 
                custom_objects={'Dense': FixDense},
                compile=False  # Avoid unnecessary compilation issues
            )
            print("--- MODEL LOADED SUCCESSFULLY ---")
        except Exception as e:
            print(f"ERROR LOADING MODEL: {str(e)}")
            return None
            
    return _model

