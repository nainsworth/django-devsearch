from django.shortcuts import render
from .models import Profile

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
