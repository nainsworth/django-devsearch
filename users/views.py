from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile

def loginUser(request):

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
