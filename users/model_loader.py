import os
import tensorflow as tf
from django.conf import settings

_model = None

def get_model():
    """
    Singleton pattern to load and cache the TensorFlow model.
    Only loads once during worker lifecycle.
    """
    global _model
    if _model is None:
        model_path = os.path.join(settings.BASE_DIR, 'models', 'herb_leaf_model.h5')
        print(f"--- INITIALIZING ML MODEL (Process: {os.getpid()}) ---")
        if not os.path.exists(model_path):
            print(f"ERROR: Model file not found at {model_path}")
            return None
        try:
            _model = tf.keras.models.load_model(model_path, compile=False)
            print("--- MODEL LOADED SUCCESSFULLY ---")
        except Exception as e:
            import traceback
            print(f"ERROR LOADING MODEL: {str(e)}")
            print(traceback.format_exc())
            return None
    return _model
