from django.shortcuts import render
from django.http import HttpResponse
from .models import Project

projectList = [
    {
        "id": "1",
        "title": "E-Commerce Website",
        "description": "Fully functional e-commerce website",
        "topRated": True,
    },
    {
        "id": "2",
        "title": "Portfolio Website",
        "description": "A personal website to write articles and display work",
        "topRated": False,
    },
    {
        "id": "3",
        "title": "Social Website",
        "description": "An open source project built by the community",
        "topRated": True,
    },
]


def projects(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, "projects/projects.html", context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    return render(request, "projects/single-project.html", {"project": projectObj})
