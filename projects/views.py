from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Project
from .forms import ProjectForm
from .utils import searchProjects


def projects(request):
    projects, search_query = searchProjects(request)

    template = "projects/projects.html"

    context = {"projects": projects, "search_query": search_query}
    return render(request, template, context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()
    reviews = projectObj.review_set.all()
    template = "projects/single-project.html"

    context = {"project": projectObj, "tags": tags, "reviews": reviews}
    return render(request, template, context)


@login_required(login_url="login")
def createProject(request):
    context = {}
    profile = request.user.profile
    form = ProjectForm()
    template = "projects/project-form.html"

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect("account")

    context["form"] = form
    return render(request, template, context)


@login_required(login_url="login")
def updateProject(request, pk):
    context = {}
    profile = request.user.profile
    projectObj = profile.project_set.get(id=pk)
    form = ProjectForm(instance=projectObj)
    template = "projects/project-form.html"

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=projectObj)
        if form.is_valid():
            form.save()
            return redirect("account")

    context["form"] = form
    return render(request, template, context)


@login_required(login_url="login")
def deleteProject(request, pk):
    context = {}
    profile = request.user.profile
    projectObj = profile.project_set.get(id=pk)
    template = "delete.html"

    if request.method == "POST":
        projectObj.delete()
        return redirect("projects")

    context["object"] = projectObj
    return render(request, template, context)
