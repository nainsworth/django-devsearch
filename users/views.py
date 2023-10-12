from django.shortcuts import render

def profiles(request):
    template = "users/profiles.html"

    return render(request, template)
