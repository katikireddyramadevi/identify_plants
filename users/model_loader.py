import os
import tensorflow as tf
from django.conf import settings

_model = None

def get_model():
    """
    Singleton pattern to load and cache the TensorFlow model.
    Only loads once during worker lifecycle.
    We rebuild the architecture and load weights only to bypass
    Keras 2/3 serialization incompatibilities.
    """
    global _model
    if _model is None:
        model_path = os.path.join(settings.BASE_DIR, 'models', 'herb_leaf_model.h5')
        print(f"--- INITIALIZING ML MODEL (Process: {os.getpid()}) ---")
        
        if not os.path.exists(model_path):
            print(f"ERROR: Model file not found at {model_path}")
            return None

        try:
            # Rebuild MobileNetV2 architecture
            base = tf.keras.applications.MobileNetV2(
                input_shape=(224, 224, 3),
                include_top=False,
                weights=None
            )
            x = base.output
            x = tf.keras.layers.GlobalAveragePooling2D()(x)
            x = tf.keras.layers.Dense(256, activation='relu', name='dense')(x)
            x = tf.keras.layers.Dropout(0.5, name='dropout')(x)
            output = tf.keras.layers.Dense(81, activation='softmax', name='dense_1')(x)
            _model = tf.keras.Model(inputs=base.input, outputs=output)

            # Load just the weights
            _model.load_weights(model_path, by_name=False)
            print("--- MODEL WEIGHTS LOADED SUCCESSFULLY ---")
        except Exception as e:
            import traceback
            print(f"ERROR LOADING MODEL WEIGHTS: {str(e)}")
            print(traceback.format_exc())
            return None

    return _model
