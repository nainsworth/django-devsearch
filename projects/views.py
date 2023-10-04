from django.shortcuts import render
from django.http import HttpResponse

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
    # name = "Nicholas Ainsworth"
    # age = 28

    context = {'projects': projectList}
    return render(request, "projects/projects.html", context)


def project(request, pk):
    projectObject = None
    for i in projectList:
        if i['id'] == str(pk):
            projectObject = i
    return render(request, "projects/single-project.html", {"project": projectObject})
