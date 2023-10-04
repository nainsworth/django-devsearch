from django.shortcuts import render
from django.http import HttpResponse

projectList = [
    {
        "id": "1",
        "title": "E-Commerce Website",
        "description": "Fully functional e-commerce website",
    },
    {
        "id": "2",
        "title": "Portfolio Website",
        "description": "A personal website to write articles and display work",
    },
    {
        "id": "3",
        "title": "Social Website",
        "description": "An open source project built by the community",
    },
]


def projects(request):
    name = "Nicholas Ainsworth"
    age = 28

    context = {"name": name, "age": age}
    return render(request, "projects/projects.html", context)


def project(request, pk):
    return render(request, "projects/single-project.html")
