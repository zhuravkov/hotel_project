import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view

from api_app.models import CustomUser
from api_app.seializers import AuthUserSerializer
from django.contrib.auth import authenticate, login,logout
# Create your views here.

def index(request):
    try:
        session_user_id = request.session['_auth_user_id']
    except:
        session_user_id = None
    try:
        username = request.__dict__['user']
    except:
        username = None
    print(session_user_id)
    print(username)
    return render (request, 'index.html', {})



@api_view(['GET'])
def authenticateApi(request):
    # auth me проверка зарегистрирован ли вользователь
    try:
        session_user_id = request.session['_auth_user_id']
    except:
        session_user_id = None

    try:
        user = CustomUser.objects.get(id=session_user_id)
        serializer = AuthUserSerializer(user)
        return JsonResponse({'data':serializer.data, 'resultCode': 0})

    except CustomUser.DoesNotExist:
        return JsonResponse({'messages': 'You are not athorized', 'resultCode': 1})



@api_view(['POST', 'DELETE'])
def apiLoginView(request):
    # LOGIN / LOGOUT in API request
    if request.method == 'POST':
        put_body = json.loads(request.body)

        email = put_body.get('email')
        password = put_body.get('password')
        print(f'email: {email}   password: {password}')

        user = authenticate(email=email, password=password)


        if user is not None:
            login(request, user)
            print(user.email)
            serializer = AuthUserSerializer(user)
            return JsonResponse({'data':serializer.data, 'resultCode': 0})

        else:
            # Return an 'invalid login' error message.
            return JsonResponse({'resultCode': 1, 'message':'No such pare email - password'})
    
    elif request.method == 'DELETE':
        logout(request)
        return JsonResponse({'resultCode': 0})
    else:
        return JsonResponse({'resultCode': 1, 'message':'something wrong'})