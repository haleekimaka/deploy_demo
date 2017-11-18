from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt, time, datetime

# Create your views here.

def index(request):
    today = datetime.date.today().strftime("%Y-%m-%d")
    request.session['today'] = today

    if 'id' in request.session:
        return redirect('/success')
    else: 
        context = {
            'today': today
        }
        return render(request, "login_reg/index.html", context)


def register(request):
    if request.method == "POST":
        print request.POST

        errors = User.objects.registration_validation(request.POST)
        
        if len(errors) > 0 :
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')

        else:
            new_pwd = bcrypt.hashpw(request.POST['pwd'].encode(), bcrypt.gensalt())

            bday = datetime.datetime.strptime(request.POST['bday'],'%Y-%m-%d')
            
            new_user = User.objects.create(first_name=request.POST['f_name'], last_name=request.POST['l_name'], birthdate=bday, email=request.POST['email'], password=new_pwd)
            request.session['id'] = new_user.id
            request.session['kind'] = "registered"
            return redirect('/success')
    else:
        messages.error(request, "Oops, something went wrong")

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validation(request.POST)
        if len(errors) > 0:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')

        else:
            logged_user = User.objects.get(email=request.POST['email'])
            request.session['id'] = logged_user.id
            request.session['kind'] = "logged in"
            return redirect('/success')
    else:
        messages.error(request,"Oops, something went wrong")

def success(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        logged_user = User.objects.get(id=request.session['id'])
        context = {
            "user": logged_user.first_name,
            "kind": request.session['kind']
        }
        return render(request, "login_reg/success.html", context)


def logout(request):
    request.session.clear()
    return redirect("/")
