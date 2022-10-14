from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import User
import bcrypt

def welcome(request):
    return render(request, 'welcome.html')

def login_reg(request):
    return render(request, 'login_reg.html')

def add_user(request):
    errors = User.objects.user_validator(request.POST, 1)
    if len(errors) > 0 :
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login_reg/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name = request.POST['first_name'],
                            last_name = request.POST['last_name'],
                            birthday = request.POST['birthday'],
                            email = request.POST['email'],
                            password = pw_hash
                            )
        request.session['first_name'] = request.POST['first_name']
        request.session['id'] = User.objects.get(email = request.POST['email']).id
        return redirect('/success')

def validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)

def render_success(request):
    try:
        request.session['first_name']
        return redirect('/dashboard')
    except:
        return redirect('/')

def log_out(request):
    if request.session['first_name']:
        del request.session['first_name']
        del request.session['id']
        try:
            del request.session['random_activity_id']
        except:
            pass
    return redirect('/')

def log_in(request):
    errors = User.objects.user_validator(request.POST, 2)
    if len(errors) > 0 :
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login_reg/')
    else:
        user = User.objects.filter(email = request.POST['login_email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['login_password'].encode(), logged_user.password.encode()):
                request.session['first_name'] = logged_user.first_name
                request.session['id'] = logged_user.id
                return redirect('/success')
            else:
                messages.error(request, 'Wrong Password! Try again')
                return redirect('/login_reg/')

#Delete before DEPLOYMENT!
def delete_all(request):
    for user in User.objects.all():
        user.delete()
    return redirect('/')

