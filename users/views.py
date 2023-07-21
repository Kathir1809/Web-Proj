from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Profiles, Skills, Message
from django.contrib import messages
from .forms import CustomUserCreation, ProfileEdit, skillsAdd, sendMessage
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .utils import searchProfiles, paginate

def profiles(request):
    profiles, search = searchProfiles(request)

    customrange, profiles = paginate(request, profiles, 3)

    return render(request, 'users/profiles.html', {'profiles':profiles, 'search':search, 'customrange':customrange} )

def userlogin(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        
        except:
            print('user does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.info(request,("You Were Successfully Logged in"))
            return redirect(request.GET['next'] if 'next' in request.GET else 'account' ) 
            
        else:
            messages.error(request,("username or password is incorrect"))

    return render(request, 'users/login_register.html')




def userlogout(request):
    logout(request)
    messages.info(request,("You Were Successfully Logged out"))
    return redirect('login')


def registeruser(request):
    page = 'register'
    form = CustomUserCreation
    context = {'page':page, 'form':form}

    if request.method == 'POST':
        form = CustomUserCreation(request.POST)
        if form.is_valid():
            form = CustomUserCreation(request.POST)
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,"Account created successfully")


            login(request, user)
            return redirect('edituser')
        
        else:
            messages.error(request,'An error occurred during registration')


    return render(request, 'users/login_register.html', context)



def userProfile(request, pk):
    userprofile = Profiles.objects.get(id=pk)
    return render(request, 'users/user-profile.html', {'p':userprofile})


@login_required(login_url='login')
def account(request):

    profile = request.user.profiles

    skills = profile.skills_set.all()

    project = profile.project_set.all()

    context = {'profile':profile, 'skills':skills, 'projects':project}

    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editaccount(request):
    profile = request.user.profiles
    form = ProfileEdit(instance=profile)


    if request.method == 'POST':
        form = ProfileEdit(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user = form.save(commit=False)
            if user.username:
                user.username = user.username.lower()
            
            user.save()

            return redirect('account')



    context = {'form':form}
    return render(request, 'users/edit.html', context)




@login_required(login_url='login')
def createskill(request):
    profile = request.user.profiles
    form = skillsAdd()

    if request.method == 'POST':
        form = skillsAdd(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('account')

    context = {'form':form}

    return render(request, 'users/skill_form.html', context)



@login_required(login_url='login')
def update_skill(request, pk):

    profile = request.user.profiles

    skill = profile.skills_set.get(id=pk)
    form = skillsAdd(instance=skill)

    if request.method == 'POST':
        form = skillsAdd(request.POST, instance=skill )
        if form.is_valid():
            form.save()
            return redirect('account')

    return render(request, 'users/skill_form.html', {'form':form})




@login_required(login_url='login')
def delete_skill(request, pk):

    profile = request.user.profiles

    skill = profile.skills_set.get(id=pk) 

    if request.method == 'POST':
        skill.delete()
        return redirect('account')

    return render(request, 'users/delete_template.html', {'object':skill.name})


@login_required(login_url='login')
def inbox(request):

    profile = request.user.profiles

    messagereq = profile.messages.all()

    unreadcount = messagereq.filter(is_read = False).count()

    context = {'messagereq':messagereq, 'unreadcount':unreadcount}

    return render(request, 'users/inbox.html', context) 




@login_required(login_url='login')
def mes(request, pk):

    profile = request.user.profiles
    
    mess = profile.messages.get(id=pk)
    
    context = {'mess':mess}

    if mess.is_read == False:
        mess.is_read = True
        mess.save()

    return render(request, 'users/message.html', context) 



@login_required(login_url='login')
def send_message(request, pk):

    recipient = Profiles.objects.get(id=pk)
    sender = request.user.profiles

    if recipient == sender:
        return redirect('account')

    form = sendMessage()

    if request.method == 'POST':
        form = sendMessage(request.POST)
        if form.is_valid:
            msg = form.save(commit=False)
            msg.sender = sender
            msg.name = sender.username
            msg.email = sender.email
            msg.receiver = recipient
            msg.save()
            messages.success(request, 'Message sent successfully')
            return redirect('userprofile', pk=recipient.id)
    
    context = {'r':recipient, 'form':form}

    return render(request, 'users/message_form.html', context)

