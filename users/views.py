from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .utils import searchProfiles, paginateProfiles


def loginUser(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("profiles")

    template = "users/login-register.html"
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("profiles")
        else:
            messages.error(request, "Username OR Password is incorrect")

    # context = {'profiles': profiles}
    return render(request, template)


def logoutUser(request):
    logout(request)
    messages.info(request, "User was logged out!")
    return redirect("login")


def registerUser(request):
    template = "users/login-register.html"
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User account was created!")
            login(request, user)
            return redirect("edit-account")

        else:
            messages.success(request, "An error has occurred")

    context = {"page": page, "form": form}
    return render(request, template, context)


def profiles(request):
    template = "users/profiles.html"
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 3)

    context = {
        "profiles": profiles,
        "search_query": search_query,
        "custom_range": custom_range,
    }
    return render(request, template, context)


def userProfiles(request, pk):
    profileObj = Profile.objects.get(id=pk)
    topSkills = profileObj.skill_set.exclude(description__exact="")
    otherSkills = profileObj.skill_set.filter(description="")
    template = "users/user-profile.html"

    context = {
        "profile": profileObj,
        "topSkills": topSkills,
        "otherSkills": otherSkills,
    }
    return render(request, template, context)


@login_required(login_url="login")
def userAccount(request):
    template = "users/account.html"
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {"profile": profile, "skills": skills, "projects": projects}
    return render(request, template, context)


@login_required(login_url="login")
def editAccount(request):
    template = "users/profile-form.html"
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect("account")

    context = {"form": form}
    return render(request, template, context)


@login_required(login_url="login")
def createSkill(request):
    template = "users/skill-form.html"
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill was added successfully!")
            return redirect("account")

    context = {"form": form}
    return render(request, template, context)


@login_required(login_url="login")
def updateSkill(request, pk):
    template = "users/skill-form.html"
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            skill.save()
            messages.success(request, "Skill was updated successfully!")

            return redirect("account")

    context = {"form": form}
    return render(request, template, context)


@login_required(login_url="login")
def deleteSkill(request, pk):
    template = "delete.html"
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill was deleted successfully!")
        return redirect("account")

    context = {"object": skill}
    return render(request, template, context)
