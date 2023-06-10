from django.shortcuts import render, redirect
from .models import Project, Tag
from .forms import ProjectForm,ReviewForm
from django.contrib.auth.decorators import login_required
from .utils import searchProjects, paginateProject
from django.contrib import messages
from django.db import IntegrityError





# projectsList = [
#     {
#         'id':'1',
#         'title':'ECommerce Website',
#         'description':'Hardware parts ecommerce website' 
#     },
#     {
#         'id':'2',
#         'title':'Portfolio Website',
#         'description':'Personal portfolio website for myself' 
#     },
#     {
#         'id':'3',
#         'title':' Business Website',
#         'description':'Business website for company' 
#     },
#     {
#         'id':'4',
#         'title':'Blog Website',
#         'description':'Blog website Bloggers' 
#     },
#     {
#         'id':'5',
#         'title':'Membership Website',
#         'description':'membership website for members'  
#     },
#     {
#         'id':'6',
#         'title':' Personal Website',
#         'description':'Personal portfolio website for myself' 
#     },
#     {
#         'id':'7',
#         'title':'Ticket Booking Website',
#         'description':'ticketbooking website for theaters' 
#     },
#     {
#         'id':'8',
#         'title':'Informational Website',
#         'description':'Informational Website website for myself' 
#     },
#     {
#         'id':'9',
#         'title':'Event Website',
#         'description':'Hardware parts ecommerce website' 
#     },
#     {
#         'id':'10',
#         'title':'Furniture Website',
#         'description':'Personal portfolio website for myself' 
#     },
    
# ]

def index(request):
    return render(request, "index.html")

def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProject(request, projects, 6)
    context = {'projects':projects, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, "projects.html", context)

@login_required(login_url='login')
def project(request, pid):
    project = Project.objects.get(id=pid)
    form = ReviewForm()
    tags = project.tags.all()
    profile = request.user.profile
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = project
            review.owner = profile
            try:
                review.save()
                messages.success(request, 'your review is saved successfully')
            except IntegrityError:
                messages.error(request, 'You have already reviewed this project')
            project.getVoteCount
            return redirect('project', pid=project.id)
    context = {'project':project,'tags':tags,'form':form}
    return render(request, "single-project.html", context)

@login_required(login_url='login')
def createProject(request):
    form = ProjectForm()
    profile = request.user.profile

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            project.owner = profile
            project.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('projects')

    context = {'form': form}
    return render(request, "project-form.html", context)


@login_required(login_url='login')
def updateProject(request, pid):
    profile = request.user.profile
    project = profile.project_set.get(id=pid)
    #project = Project.objects.get(id=pid)
    form = ProjectForm(instance=project)


    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            project.owner = profile
            project.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('projects')
    context = {'form': form,'project':project}
    return render(request, "project-form.html", context)

@login_required(login_url='login')
def deleteProject(request, pid):
    profile = request.user.profile
    project = profile.project_set.get(id=pid)

    if request.method == 'POST':
        project.delete()
        return redirect('account')

    context = {'project': project}
    return render(request, "delete-template.html", context)


        



