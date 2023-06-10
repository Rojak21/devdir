from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from .models import Profile, Skill
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib.auth.decorators import login_required
from .utils import searchProfiles, paginateProfiles


# Create your views here.


def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 6)
    context = {'profiles': profiles,'search_query': search_query,'custom_range': custom_range}
    return render(request, 'profiles.html', context)


def userProfile(request, pid):
    profile = Profile.objects.get(id=pid)
    topSkills = profile.skill_set.exclude(description__exact='')
    otherSkills = profile.skill_set.filter(description='')
    context = {'profile': profile , 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'user-profile.html', context)

def loginUser(request):
    page = 'login'
    context = {'page': page}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username == "" or password == "":
            messages.error(request, 'Username or password is required')
            return render(request,'login_register.html',context)
        
        try: 
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
            return render(request,'login_register.html',context)
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('account')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login_register.html',context)
    
def logoutUser(request):
    logout(request)
    messages.info(request, 'User logged out')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            
            messages.success(request, f'Account created for {user}')
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, f'Could not create account.')
    context = {'page': page,'form': form}
    return render(request,'login_register.html',context)

def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {'profile':profile , 'skills':skills, 'projects':projects}
    return render(request,'account.html',context)

def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account updated for {request.user}')
            return redirect('account')
        else:
            messages.error(request, f'Could not update account.')
    context ={'form':form}
    return render(request,'profile_form.html',context)

def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, f'Skill created for {request.user}')
            return redirect('account')
        else:
            messages.error(request, f'Could not create skill.')
    context ={'form':form}
    return render(request,'skill_form.html',context)

login_required(login_url='login')
def updateSkill(request, sid):
    profile = request.user.profile
    skill = profile.skill_set.get(id=sid)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, "skill_form.html", context)

@login_required(login_url='login')
def deleteSkill(request, sid):
    profile = request.user.profile
    skill = profile.skill_set.get(id=sid)
    if request.method == 'POST':
        skill.delete()
        return redirect('account')
    context = {'object': skill}
    return render(request, "delete-template.html", context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests,'unreadCount': unreadCount}
    return render(request, 'inbox.html', context)

@login_required(login_url='login')
def viewMessage(request, mid):
    profile = request.user.profile
    message = profile.messages.get(id=mid)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message':message}
    return render(request, 'message.html', context)


def createMessage(request, pid):
    recipient = Profile.objects.get(id=pid)
    form = MessageForm()
    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
            messages.success(request, f'Message sent to {recipient}')
            return redirect('user-profile',pid=recipient.id)
        else:
            messages.error(request, f'Could not send message.')

    context = {'form': form, 'recipient':recipient}
    return render(request, 'message_form.html', context)










