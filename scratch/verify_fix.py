import os
import sys
import django
from pathlib import Path

# Setup Django environment
sys.path.append(str(Path(r'c:\Users\Surya teja\rama\identify_plants')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'identify_plants_and_its_Medicinal_properties.settings')
django.setup()

from users.model_loader import get_model

def verify():
    print("Attempting to load model via get_model()...")
    model = get_model()
    if model:
        print("SUCCESS: Model loaded correctly!")
        print(f"Input shape: {model.input_shape}")
        print(f"Output shape: {model.output_shape}")
    else:
        print("FAILED: Model could not be loaded.")

if __name__ == "__main__":
    verify()
