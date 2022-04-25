from django.shortcuts import render

# Create your views here.

def index(request):
    try:
        request.session['_auth_user_id']
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