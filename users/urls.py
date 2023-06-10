from django.urls import path
from . import views


urlpatterns = [
    path('', views.profiles, name="profiles"),
    path('user-profile/<str:pid>/', views.userProfile, name="user-profile"),

    path('login/',views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    
   
    path('account/', views.userAccount, name="account"),
    path('edit-account/', views.editAccount, name="edit-account"),

    path('create-skill/', views.createSkill, name="create-skill"),
    path("update-skill/<str:sid>/", views.updateSkill, name="update-skill"),
    path("delete-skill/<str:sid>/", views.deleteSkill, name="delete-skill"),

    path('inbox/', views.inbox, name="inbox"),
    path('message/<str:mid>/', views.viewMessage, name="message"),
    path('create-message/<str:pid>/', views.createMessage,name="create-message"),

]
