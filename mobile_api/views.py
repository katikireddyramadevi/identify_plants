import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from users.models import UserRegistrationModel
from users.views import class_names, descriptions

@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            loginid = data.get('loginid', '').strip()
            pswd = data.get('password', '').strip()
            
            print(f"--- LOGIN ATTEMPT ---")
            print(f"LoginID: [{loginid}]")
            print(f"Password: [{pswd}]")
            
            try:
                user = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
                print(f"User Found: {user.name}, Status: {user.status}")
                if user.status == "activated":
                    return JsonResponse({
                        'status': 'success',
                        'user': {
                            'id': user.id,
                            'name': user.name,
                            'loginid': user.loginid,
                            'email': user.email
                        }
                    })
                else:
                    return JsonResponse({'status': 'error', 'message': 'Account not activated'}, status=401)
            except UserRegistrationModel.DoesNotExist:
                print(f"Login Failed: User not found or password incorrect")
                return JsonResponse({'status': 'error', 'message': 'Invalid loginid or password'}, status=401)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)

@csrf_exempt
def api_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            UserRegistrationModel.objects.create(
                name=data.get('name'),
                loginid=data.get('loginid'),
                password=data.get('password'),
                mobile=data.get('mobile'),
                email=data.get('email'),
                locality=data.get('locality'),
                address=data.get('address'),
                city=data.get('city'),
                state=data.get('state'),
                status='activated'
            )
            return JsonResponse({'status': 'success', 'message': 'Registration successful'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)

from PIL import Image, ImageOps

@csrf_exempt
def api_predict(request):
    import numpy as np
    import tensorflow as tf
    
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image_file = request.FILES['image']
            image_path = os.path.join(settings.MEDIA_ROOT, 'mobile_' + image_file.name)
            
            with open(image_path, 'wb+') as f:
                for chunk in image_file.chunks():
                    f.write(chunk)
            
            # Try 13MB model with 150x150
            model_path = os.path.join(settings.MEDIA_ROOT, 'herb_leaf_model.h5')
            json_path  = os.path.join(settings.MEDIA_ROOT, 'graph/class_labels.json')
            
            with open(json_path, "r") as f:
                class_labels = json.load(f)
            
            # Open and fix orientation
            img = Image.open(image_path).convert('RGB')
            img = ImageOps.exif_transpose(img) 
            # Fix Resize to 224x224 for this model
            img = img.resize((224, 224))
            
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            model = tf.keras.models.load_model(model_path)
            preds = model.predict(img_array)
            predicted_index = np.argmax(preds)
            predicted_class = class_labels[str(predicted_index)]
            
            # TOP 5 DEBUG
            top_5_indices = np.argsort(preds[0])[-5:][::-1]
            print(f"--- PREDICTION DEBUG (v3) ---")
            print(f"Model: {model_path}")
            print(f"Input: {img_array.shape}")
            print(f"Top 5 Guesses:")
            for idx in top_5_indices:
                name = class_labels.get(str(idx), "Unknown")
                prob = preds[0][idx]
                print(f"  - {name}: {prob:.4f}")
            print(f"----------------------------")
            
            description = descriptions.get(predicted_class, "No description available.")
            
            return JsonResponse({
                'status': 'success',
                'predicted_class': predicted_class,
                'description': description,
                'image_url': f"/media/mobile_{image_file.name}",
                'confidence': float(np.max(preds)),
                'top_guesses': [class_labels.get(str(idx)) for idx in top_5_indices]
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Image required'}, status=400)
