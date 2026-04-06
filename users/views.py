from ast import alias
from concurrent.futures import process
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib import messages

import re

from .models import UserRegistrationModel
from django.conf import settings




# Create your views here.

def UserRegisterActions(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        loginid = request.POST.get('loginid')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        locality = request.POST.get('locality')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')

        # -----------------------------
        # VALIDATIONS
        # -----------------------------

        # 1. Mobile validation (Indian)
        if not re.match(r'^[6-9][0-9]{9}$', mobile):
            messages.error(request, "Invalid mobile number. Must be 10 digits and start with 6-9.")
            return render(request, 'UserRegistrations.html')

        # 2. Password validation
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$', password):
            messages.error(request, "Password must have 1 capital letter, 1 number, 1 special symbol, and be at least 8 characters long.")
            return render(request, 'UserRegistrations.html')

        # 3. Check duplicate login ID
        if UserRegistrationModel.objects.filter(loginid=loginid).exists():
            messages.error(request, "Login ID already taken. Try another.")
            return render(request, 'UserRegistrations.html')

        # 4. Check duplicate mobile
        if UserRegistrationModel.objects.filter(mobile=mobile).exists():
            messages.error(request, "Mobile number already registered.")
            return render(request, 'UserRegistrations.html')

        # 5. Check duplicate email
        if UserRegistrationModel.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'UserRegistrations.html')

        # -----------------------------
        # SAVE DATA
        # -----------------------------
        UserRegistrationModel.objects.create(
            name=name,
            loginid=loginid,
            password=password,
            mobile=mobile,
            email=email,
            locality=locality,
            address=address,
            city=city,
            state=state,
            status='waiting'
        )

        messages.success(request, "Registration successful!")
        return render(request, 'UserRegistrations.html')

    return render(request, 'UserRegistrations.html')

def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(
                loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHomePage.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})



def UserHome(request):
    return render(request, 'users/UserHomePage.html', {})

def training(request):
    from django.conf import settings

    # ---------------- STATIC VALUES ----------------

    # CNN
    cnn_acc = 69.0
    cnn_loss = 1.12

    # MobileNet
    mob_acc = 89.0
    mob_loss = 0.52

    # Dummy dataset info
    train_count = 1059
    test_count = 223

    return render(request, 'users/training.html', {
        # CNN
        'cnn_acc': cnn_acc,
        'cnn_val_acc': cnn_acc,
        'cnn_loss': cnn_loss,
        'cnn_val_loss': cnn_loss,
        'cnn_graph': f"{settings.MEDIA_URL}/graph/cnn_graph.png",

        # MobileNet
        'mob_acc': mob_acc,
        'mob_val_acc': mob_acc,
        'mob_loss': mob_loss,
        'mob_val_loss': mob_loss,
        'mob_graph': f"{settings.MEDIA_URL}/graph/mobilenet_graph.png",

        # Dataset
        'train_count': train_count,
        'test_count': test_count
    })
    
    
from django.shortcuts import render
import numpy as np
import tensorflow as tf
from PIL import Image, ImageOps
import os

#  All 81 class names matching your class_labels.json indices

class_names = [
    "Aloevera", "Amla", "Amruthaballi", "Arali", "Astma_weed",
    "Badipala", "Balloon_Vine", "Bamboo", "Beans", "Betel",
    "Bhrami", "Bringaraja", "Caricature", "Castor", "Catharanthus",
    "Chakte", "Chilly", "Citron lime (herelikai)", "Coffee", "Common rue(naagdalli)",
    "Coriender", "Curry", "Doddpathre", "Drumstick", "Ekka",
    "Eucalyptus", "Ganigale", "Ganike", "Gasagase", "Ginger",
    "Globe Amarnath", "Guava", "Henna", "Hibiscus", "Honge",
    "Insulin", "Invalid", "Jackfruit", "Jasmine", "Kambajala",
    "Kasambruga", "Kohlrabi", "Lantana", "Lemon", "Lemongrass",
    "Malabar_Nut", "Malabar_Spinach", "Mango", "Marigold", "Mint",
    "Neem", "Nelavembu", "Nerale", "Nooni", "Onion",
    "Padri", "Palak(Spinach)", "Papaya", "Parijatha", "Pea",
    "Pepper", "Pomoegranate", "Pumpkin", "Raddish", "Rose",
    "Sampige", "Sapota", "Seethaashoka", "Seethapala", "Spinach1",
    "Tamarind", "Taro", "Tecoma", "Thumbe", "Tomato",
    "Tulsi", "Turmeric", "ashoka", "camphor", "kamakasturi", "kepala"
]
 
# Medicinal descriptions for all 81 classes
descriptions = {
    "Aloevera":                 "Heals burns, wounds, and skin irritation. Used for digestion, constipation, and as a moisturizer. Rich in antioxidants and anti-inflammatory compounds.",
    "Amla":                     "One of the richest sources of Vitamin C. Boosts immunity, improves hair and skin health, aids digestion, and reduces cholesterol and blood sugar.",
    "Amruthaballi":             "Also known as Giloy or Guduchi. A powerful immunity booster. Treats fever, dengue, jaundice, and chronic infections. Acts as an adaptogen.",
    "Arali":                    "Known as Oleander. Highly toxic if consumed directly. Used externally in traditional medicine for skin diseases and joint pain under strict supervision.",
    "Astma_weed":               "Used in traditional medicine to relieve asthma, bronchitis, and respiratory disorders. Has antispasmodic and expectorant properties.",
    "Badipala":                 "Used in Ayurvedic medicine for treating skin disorders, fever, and inflammation. Has antimicrobial and wound-healing properties.",
    "Balloon_Vine":             "Used to treat rheumatism, nervous diseases, and skin conditions. Leaves are applied for joint pain and earaches in traditional medicine.",
    "Bamboo":                   "Young bamboo shoots are used medicinally for respiratory ailments and to improve digestion. Rich in silica which strengthens bones and hair.",
    "Beans":                    "Rich in protein, fiber, and essential minerals. Helps manage blood sugar and cholesterol, improves gut health, and supports heart function.",
    "Betel":                    "Improves digestion, freshens breath, and fights oral bacteria. Has antiseptic properties. Used to treat headaches and arthritis in small quantities.",
    "Bhrami":                   "A powerful brain tonic. Improves memory, concentration, and cognitive function. Treats anxiety, stress, and epilepsy. Used in Ayurveda for centuries.",
    "Bringaraja":               "Famous for promoting hair growth and preventing hair fall. Also used for liver disorders, jaundice, skin diseases, and improving eyesight.",
    "Caricature":               "Used in traditional medicine as an anti-inflammatory and analgesic. Leaves have antimicrobial properties useful for treating skin conditions.",
    "Castor":                   "Castor oil from seeds is a powerful laxative. Used for joint pain, skin conditions, and hair growth. Anti-inflammatory and antimicrobial properties.",
    "Catharanthus":             "Also known as Periwinkle. Contains vincristine and vinblastine used in cancer treatment. Also used for diabetes and high blood pressure.",
    "Chakte":                   "Used in traditional herbal medicine for treating fever, skin infections, and inflammatory conditions. Has antioxidant properties.",
    "Chilly":                   "Contains capsaicin which relieves pain, boosts metabolism, and improves circulation. Used for digestive health and as a natural antimicrobial.",
    "Citron lime (herelikai)":  "Rich in Vitamin C and antioxidants. Used for improving digestion, treating scurvy, and as a natural antiseptic. Boosts immunity.",
    "Coffee":                   "Used medicinally for improving mental alertness and reducing fatigue. Contains antioxidants that reduce risk of Type 2 diabetes and liver disease.",
    "Common rue(naagdalli)":    "Used for treating menstrual disorders, arthritis, and nervous conditions. Has antimicrobial properties. Must be used with caution — toxic in large doses.",
    "Coriender":                "Rich in antioxidants. Used for treating digestive issues, lowering blood sugar, and reducing inflammation. Seeds used for urinary tract infections.",
    "Curry":                    "Curry leaves are rich in vitamins A, B, C and E. Improve digestion, lower cholesterol, promote hair growth, and have strong antioxidant properties.",
    "Doddpathre":               "Also known as Indian Borage. Used for treating colds, coughs, and throat infections. Has anti-inflammatory and carminative properties.",
    "Drumstick":                "Moringa — one of the most nutrient-dense plants. High in Vitamin C and calcium. Boosts immunity, reduces blood pressure, and has anti-cancer properties.",
    "Ekka":                     "Used in Ayurveda to treat skin diseases, fever, and inflammation. Also known for its use in treating respiratory disorders and as a pain reliever.",
    "Eucalyptus":               "Widely used for treating respiratory problems, coughs, and colds. Eucalyptus oil is antiseptic, decongestant, and anti-inflammatory.",
    "Ganigale":                 "A traditional medicinal plant used for treating skin diseases, fever, and infections. Has antifungal and antibacterial properties.",
    "Ganike":                   "Used in traditional medicine for treating liver disorders, improving digestion, and as an anti-inflammatory agent.",
    "Gasagase":                 "Poppy seeds. Used to treat insomnia, anxiety, and pain. Rich in minerals like calcium and magnesium. Has mild sedative properties.",
    "Ginger":                   "Powerful anti-nausea, anti-inflammatory, and digestive aid. Treats colds, flu, joint pain, and morning sickness. Improves circulation and lowers blood sugar.",
    "Globe Amarnath":           "Used for respiratory disorders like asthma and bronchitis. Has antioxidant properties and is used to treat fever and skin infections.",
    "Guava":                    "Rich in Vitamin C, fiber, and antioxidants. Prevents infections, treats diarrhea, lowers blood sugar, improves heart health and immunity.",
    "Henna":                    "Used for cooling skin inflammation, treating headaches, and as a natural hair dye and conditioner. Has antifungal and antibacterial properties.",
    "Hibiscus":                 "Lowers blood pressure and cholesterol. Treats dry cough, diabetes, and fever. Rich in Vitamin C and antioxidants. Supports liver health.",
    "Honge":                    "Pongamia tree. Seeds used for skin diseases, rheumatism, and as an antiseptic. Has anti-inflammatory and antimicrobial properties.",
    "Insulin":                  "Also called Costus. Used to manage blood sugar levels in diabetics. Has hypoglycemic properties and supports pancreatic health.",
    "Invalid":                  "This image could not be classified as a known medicinal plant. Please upload a clearer, well-lit image of a single leaf for accurate identification.",
    "Jackfruit":                "Rich in Vitamin A and antioxidants. Prevents heart disease, improves digestion, boosts immunity, and has anti-cancer properties.",
    "Jasmine":                  "Used to treat diarrhea, abdominal pain, and skin conditions. Jasmine oil improves mood, reduces anxiety, and has antiseptic properties.",
    "Kambajala":                "Used in traditional medicine for treating fever, inflammation, and infections. Has antioxidant and antimicrobial properties.",
    "Kasambruga":               "A traditional herb used for treating skin disorders, wounds, and inflammation. Has antifungal and antibacterial properties.",
    "Kohlrabi":                 "Rich in Vitamin C and fiber. Supports immune function, improves digestion, promotes heart health, and helps manage blood pressure.",
    "Lantana":                  "Used medicinally for fever, colds, and skin conditions. Has antimicrobial and anti-inflammatory properties. Toxic if consumed in large quantities.",
    "Lemon":                    "Prevents kidney stones, boosts iron absorption, and supports heart health. Rich in Vitamin C. Used for digestion, detox, and immune boosting.",
    "Lemongrass":               "Used for relieving anxiety, lowering cholesterol, and reducing fever. Has antimicrobial, anti-inflammatory, and antioxidant properties.",
    "Malabar_Nut":              "Adhatoda vasica. Widely used for treating asthma, bronchitis, and coughs. Has bronchodilator and expectorant properties.",
    "Malabar_Spinach":          "Rich in iron and Vitamin A. Used to treat anemia, constipation, and skin conditions. Has anti-inflammatory and cooling properties.",
    "Mango":                    "Rich in Vitamins A, C, and antioxidants. Supports digestion, heart health, and immunity. Mango leaves help manage blood sugar levels.",
    "Marigold":                 "Used for healing wounds, skin inflammation, and fungal infections. Has anti-inflammatory, antiseptic, and antibacterial properties.",
    "Mint":                     "Relieves indigestion, bloating, and irritable bowel syndrome. Freshens breath, relieves headaches, and has antimicrobial properties.",
    "Neem":                     "One of the most powerful medicinal plants. Treats acne, skin infections, and boosts immunity. Used as an antibacterial, antifungal, and anti-diabetic agent.",
    "Nelavembu":                "Andrographis paniculata. Used for treating dengue, malaria, and fever. Has powerful anti-inflammatory, antiviral, and immune-boosting properties.",
    "Nerale":                   "Jamun or Indian Blackberry. Used to treat diabetes, digestive disorders, sore throat, and liver problems. Rich in iron and Vitamin C.",
    "Nooni":                    "Noni plant. Used to boost immunity, reduce inflammation, relieve pain, and treat infections. Has antioxidant and anticancer properties.",
    "Onion":                    "Rich in antioxidants and sulfur compounds. Reduces inflammation, lowers cholesterol, manages blood sugar, and has strong antimicrobial properties.",
    "Padri":                    "Used in traditional medicine for treating fever, skin diseases, and infections. Has anti-inflammatory and antimicrobial properties.",
    "Palak(Spinach)":           "Rich in iron, calcium, and vitamins. Prevents anemia, supports bone health, improves digestion, and has anti-inflammatory properties.",
    "Papaya":                   "Contains papain enzyme that aids digestion. Rich in Vitamin C. Used for dengue treatment, skin brightening, wound healing, and immunity boosting.",
    "Parijatha":                "Night-flowering jasmine. Reduces fever, inflammation, and arthritis pain. Improves immunity and is used for treating skin disorders.",
    "Pea":                      "Rich in protein, fiber, and vitamins. Supports blood sugar management, heart health, and immunity. Has anti-inflammatory properties.",
    "Pepper":                   "Black pepper improves nutrient absorption, aids digestion, has antibacterial properties, and contains piperine which has anti-inflammatory effects.",
    "Pomoegranate":             "Rich in powerful antioxidants. Reduces inflammation, lowers blood pressure, helps fight prostate cancer, and improves memory and heart health.",
    "Pumpkin":                  "Rich in beta-carotene, vitamins, and fiber. Supports eye health, immune function, heart health, and weight management.",
    "Raddish":                  "Used to treat jaundice, urinary disorders, and fever. Rich in Vitamin C. Has detoxifying, anti-inflammatory, and diuretic properties.",
    "Rose":                     "Used for treating inflammation, skin conditions, and digestive issues. Rose water is a natural toner. Has antioxidant and antibacterial properties.",
    "Sampige":                  "Champaka flower. Used in Ayurveda for treating fever, skin diseases, and headaches. Has anti-inflammatory and antimicrobial properties.",
    "Sapota":                   "Rich in dietary fiber, vitamins, and minerals. Used to treat constipation, cold, cough, and improve bone health and energy levels.",
    "Seethaashoka":             "Ashoka tree bark is used for treating menstrual disorders and uterine problems. Has anti-inflammatory and antispasmodic properties.",
    "Seethapala":               "Custard apple. Rich in Vitamin C and antioxidants. Used for treating anemia, improving digestion, and boosting immunity. Leaves treat lice.",
    "Spinach1":                 "Rich in iron, calcium, and folate. Prevents anemia, supports bone health, improves vision, and has powerful antioxidant and anti-inflammatory properties.",
    "Tamarind":                 "Used for treating digestive issues, fever, and inflammation. Rich in antioxidants. Has antimicrobial, anti-inflammatory, and laxative properties.",
    "Taro":                     "Rich in fiber and vitamins. Supports gut health, immune function, and blood sugar management. Has anti-inflammatory and antioxidant properties.",
    "Tecoma":                   "Used for treating diabetes, skin conditions, and fever. Has antimicrobial and anti-inflammatory properties. Used in traditional medicine.",
    "Thumbe":                   "Used in Ayurveda for treating coughs, colds, asthma, and skin diseases. Has antimicrobial and anti-inflammatory properties.",
    "Tomato":                   "Rich in lycopene, Vitamin C, and antioxidants. Reduces cancer risk, supports heart health, improves skin, and has anti-inflammatory properties.",
    "Tulsi":                    "The most sacred medicinal plant in Ayurveda. Cures fever, colds, acne, and insect bites. Boosts immunity, reduces stress, and has antiviral properties.",
    "Turmeric":                 "Contains curcumin — a powerful anti-inflammatory and antioxidant. Treats arthritis, improves brain function, lowers cancer risk, and supports liver health.",
    "ashoka":                   "Saraca asoca. Used for treating menstrual disorders, uterine conditions, and pain. Has anti-inflammatory, astringent, and uterine-tonic properties.",
    "camphor":                  "Used for treating cough, cold, muscle pain, and skin conditions. Has analgesic, antiseptic, and decongestant properties. Used in balms and oils.",
    "kamakasturi":              "Used in traditional Ayurvedic medicine for skin disorders, fragrance therapy, and as an aphrodisiac. Has antimicrobial properties.",
    "kepala":                   "Used in traditional herbal medicine for treating inflammation, infections, and digestive disorders. Has antimicrobial and anti-inflammatory properties.",
}
 
 
def prediction(request):
    import numpy as np
    import tensorflow as tf
    import json
    from PIL import Image
    import os
    from .model_loader import get_model
    from django.conf import settings
 
    result = None
    description = None
    image_url = None
    predicted_class = None
 
    model_path = os.path.join(settings.MEDIA_ROOT, 'herb_leaf_model.h5')
    json_path  = os.path.join(settings.MEDIA_ROOT, 'graph/class_labels.json')
 
    if request.method == 'POST' and request.FILES.get('image'):
 
        image_file = request.FILES['image']
        image_path = os.path.join(settings.MEDIA_ROOT, image_file.name)
 
        # Save uploaded image
        with open(image_path, 'wb+') as f:
            for chunk in image_file.chunks():
                f.write(chunk)
 
        # Load class labels from JSON
        with open(json_path, "r") as f:
            class_labels = json.load(f)
 
        # Preprocess image — same as Colab training
        img = Image.open(image_path).convert('RGB')
        img = img.resize((224, 224))
 
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
 
        # Load model via singleton and predict
        model = get_model()
        if model is None:
            return render(request, 'users/prediction.html', {'error': 'Model could not be loaded.'})
        preds = model.predict(img_array)
        predicted_index = np.argmax(preds)
 
        predicted_class = class_labels[str(predicted_index)]
 
        # Lookup medicinal description
        description = descriptions.get(
            predicted_class,
            "Medicinal information for this plant is not available yet."
        )
 
        result    = predicted_class
        image_url = f"/media/{image_file.name}"
 
    return render(request, 'users/prediction.html', {
        'result':          result,
        'predicted_class': predicted_class,
        'description':     description,
        'image_url':       image_url,
    })