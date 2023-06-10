from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("projects/", views.projects, name="projects"),
    path("project/<str:pid>", views.project, name="project"),
    path("create-project", views.createProject, name="create-project"),
    path("update-project/<str:pid>", views.updateProject, name="update-project"),
    path("delete-project/<str:pid>", views.deleteProject, name="delete-project"),
]
