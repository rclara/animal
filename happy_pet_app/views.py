from django.shortcuts import render, redirect
from django.contrib import messages
from.models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def register_user(request):
    if request.method == "GET":
        return render(request, "register.html")
    if request.method == "POST":
        post_data = request.POST
        errors = User.objects.registration_validator(post_data)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect("/")
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                phone = request.POST['phone'],
                password = hashed_pw
            )
            new_user = User.objects.last()
            request.session['userid'] = new_user.id
            return redirect("/success", new_user)

def success(request):
    return render(request, "success.html")

def forgot(request):
    return render(request, "credentials.html")

def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        post_data = request.POST
        errors = User.objects.login_validator(post_data)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect("/login")
        else:
            potential_user = User.objects.filter(email = request.POST['login_email'])[0]
            if bcrypt.checkpw(request.POST['login_password'].encode(), potential_user.password.encode()):
                request.session['userid'] = potential_user.id 
                #setting session key 'userid' to value of the user logging in (id)
            return redirect("/dashboard")

def logout(request):
    request.session.clear()
    return redirect("/")
#######################################################################
def dashboard(request):
    if 'userid' not in request.session:
        return redirect("/login")
    context = {
        "logged_user": User.objects.get(id = request.session['userid']),
        "pets": Pet.objects.all()
        #context dict, key 'logged_user' with the value of the user object logged in
    }
    print(context['pets'])
    return render(request, "dashboard.html", context)


def register_pet(request):
    if request.method == "GET":
        return render(request, "pet.html")
    if request.method == "POST":
        post_data = request.POST
        errors = Pet.objects.pet_registration_validator(post_data)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect("/add_pet")
        else:
            logged_user = User.objects.get(id = request.session['userid'])
            Pet.objects.create(
                name = request.POST['name'],
                species = request.POST['species'],
                breed = request.POST['breed'],
                date_of_birth = request.POST['date_of_birth'],
                comments = request.POST['comments'],
                owner = logged_user
            )
            print(Pet.objects.last())
        return redirect("/dashboard")

def pet_portal(request, id):
    context = {
        "pet": Pet.objects.get(id=id)
    }
    print(context['pet'])
    return render(request, "portal.html", context)

def daily_log(request, id):
    context = {
        "pet": Pet.objects.get(id=id)
    }
    print(context['pet'])
    return render(request, "daily_log.html", context)