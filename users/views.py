from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')


    template = "users/login-register.html"
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try: 
            user = User.objects.get(username = username)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username OR Password is incorrect')

    # context = {'profiles': profiles}
    return render(request, template)

def logoutUser(request):
    logout(request)
    messages.error(request, 'User was logged out!')
    return redirect("login")

def registerUser(request):
    template = "users/login-register.html"
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')
            login(request, user)
            return redirect('profiles')
        
        else:
            messages.success(request, 'An error has occurred')

    context = {'page': page, 'form': form}
    return render(request, template, context)


def profiles(request):
    template = "users/profiles.html"
    profiles = Profile.objects.all()

    context = {'profiles': profiles}
    return render(request, template, context)

def userProfiles(request, pk):
    profileObj = Profile.objects.get(id=pk)
    topSkills = profileObj.skill_set.exclude(description__exact="")
    otherSkills = profileObj.skill_set.filter(description="")
    template = "users/user-profile.html"

    context = {'profile': profileObj, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, template, context)
