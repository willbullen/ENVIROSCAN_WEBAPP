from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm, UserUpdateForm, ProfileUpdateForm

from .models import Organization
import json

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":        
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "page_login.html", {"form": form, "msg" : msg})

def register_user(request):

    msg     = None
    success = False
    organizations = {}
    
    if request.method == "POST":

        u_form = SignUpForm(request.POST)
        p_form = ProfileUpdateForm(request.POST)        

        if u_form.is_valid() and p_form.is_valid():

            organization = p_form.cleaned_data.get("organization")

            u_form.save()

            username = u_form.cleaned_data.get("username")
            raw_password = u_form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            profile = p_form.save(commit=False)
            profile.user = user
            profile.save()

            msg     = 'User created - please <a href="/login">login</a>.'
            success = True
            
            return redirect("/")
        else:
            msg = 'Form is not valid'    
    else:
        u_form = SignUpForm()

    organizations = Organization.objects.all()

    return render(request, "page_register.html", {"form": u_form, "msg" : msg, "success" : success, "list_organizations" : organizations })

@login_required
def profile(request):
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        print(request.user)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)
