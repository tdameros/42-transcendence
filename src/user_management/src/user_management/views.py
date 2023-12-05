from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User

def hello(request):
    return JsonResponse({'message': 'Hello from user_management!'})

@csrf_exempt
def login(request):

    print("login api requested")

    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            name = json_data.get('name', '')
            return JsonResponse({'message': f'Welcome! {name}'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format'}, status=400)
    if request.method == "GET":
        return JsonResponse({'message': 'Expected POST method, received GET ...'})


def encode(request):
    # Payload : Les données à inclure dans le JWT
    user_id = 42

    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1),  # Date d'expiration du JWT
        'iat': datetime.utcnow()  # Date de création du JWT
        # Vous pouvez ajouter d'autres données au besoin
    }

    # Création du JWT en utilisant la clé secrète de votre application Django
    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return JsonResponse({"jwt": f"{jwt_token}"})


@csrf_exempt
def decode(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            encoded_jwt = json_data.get('encoded_jwt', '')
            try:
                decoded_payload = jwt.decode(encoded_jwt, settings.SECRET_KEY, algorithms=["HS256"])
                return JsonResponse(decoded_payload)
            except:
                return JsonResponse({'message': 'invalid JWT'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format'}, status=400)
    if request.method == "GET":
        return JsonResponse({'message': '(decode)Expected POST method, received GET ...'})


@csrf_exempt
def signup(request):
    print("signup..")
    if request.method == "POST":
        # try:
        print("here")
        json_data = json.loads(request.body.decode('utf-8'))
        required_attributes = ['firstname', 'lastname', 'email', 'password', 'username']
        # Check if all required attributes exist in the JSON data
        if all(attr in json_data for attr in required_attributes):
            firstname = json_data['firstname']
            lastname = json_data['lastname']
            email = json_data['email']
            password = json_data['password']
            username = json_data['username']
            user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname,
                                            password=password, email=email)
            user.save()
            return JsonResponse({'message': 'signup with successful'})
        else:
            missing_attributes = [attr for attr in required_attributes if attr not in json_data]
            return JsonResponse({'message': f'Missing attributes: {missing_attributes}'}, status=400)
        # except:
        #     # return JsonResponse({'message': 'Invalid JSON format'}, status=400)
    if request.method == "GET":
        return JsonResponse({'message': '(signup)Expected POST method, received GET ...'})
