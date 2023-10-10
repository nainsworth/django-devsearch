from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm


def projects(request):
    projects = Project.objects.all()
    context = {"projects": projects}
    return render(request, "projects/projects.html", context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()
    reviews = projectObj.review_set.all()
    template = "projects/single-project.html"
    
    context = {"project": projectObj, "tags": tags, "reviews": reviews}
    return render(request, template, context)


def createProject(request):
    context = {}
    form = ProjectForm()
    template = "projects/project-form.html"

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("projects")

    context["form"] = form
    return render(request, template, context)


def updateProject(request, pk):
    context = {}
    projectObj = Project.objects.get(id=pk)
    form = ProjectForm(instance=projectObj)
    template = "projects/project-form.html"

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=projectObj)
        if form.is_valid():
            form.save()
            return redirect("projects")

    context['form'] = form
    return render(request, template, context)
