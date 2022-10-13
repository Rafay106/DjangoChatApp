from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from . models import *
from . forms import RoomCreateForm, UserForm, MyUserCreationForm

# Create your views here.

def loginUser(request):
    page = 'login'

    if  request.user.is_authenticated:
        return redirect('chat:homeView')

    if request.method == 'POST':
        e_mail = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = UserModel.objects.get(email=e_mail)
        except:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, email=e_mail, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('chat:homeView')
        else:
            messages.error(request, 'Username or Password does not exist!')

    context = {
        'page' : page
    }
    return render(request, 'chat/login&register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('chat:loginUser')

def registerUser(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('chat:homeView')
        else:
            messages.error(request, 'Error occured')
    context = {
        'form' : form
    }
    return render(request, 'chat/login&register.html', context)

def homeView(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = RoomModel.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(description__icontains=q)
    )
    topics = TopicModel.objects.all()[0:5]
    msgs = MessageModel.objects.filter(Q(room__topic__name__icontains=q ))

    context = {
        'rooms'      : rooms,
        'topics'     : topics,
        'msgs'       : msgs
    }
    return render(request, 'chat/homeView.html', context)

def roomView(request, pk):
    room = get_object_or_404(RoomModel, id=pk)
    msgs = room.messagemodel_set.all()
    participants_list = room.participants.all()

    if request.method == 'POST':
        message = MessageModel.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('msgbody')
        )
        room.participants.add(request.user)
        return redirect('chat:roomView', pk=room.id)

    context = {
        "room" : room,
        "msgs" : msgs,
        "participants" : participants_list
    }
    return render(request, 'chat/roomView.html', context)

def userProfileView(request, uname):
    user = UserModel.objects.get(username=uname)
    rooms = user.roommodel_set.all()
    topics = TopicModel.objects.all()[0:5]
    msgs = user.messagemodel_set.all()
    context = {
        'user' : user,
        'rooms' : rooms,
        'topics' : topics,
        'msgs' : msgs
    }
    return render(request, 'chat/user_profile.html', context)

@login_required(login_url='chat:loginUser')
def createView(request):
    form = RoomCreateForm()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = TopicModel.objects.get_or_create(name = topic_name)
        room = RoomModel.objects.create(
            host        = request.user,
            topic       = topic,
            name        = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('chat:roomView', pk=room.id)

    f_title = "Create Room"
    topics = TopicModel.objects.all()

    context = {
        "form"    : form,
        "f_title" : f_title,
        "topics"  : topics
    }
    return render(request, 'chat/roomCreateForm.html', context)

@login_required(login_url='chat:loginUser')
def updateView(request, pk):
    room = get_object_or_404(RoomModel, id=pk)
    form = RoomCreateForm(instance=room)
    topics = TopicModel.objects.all()

    if request.user != room.host:
        return HttpResponse('Oops! Action not allowed.')

    if request.method == 'POST':
        topic_name       = request.POST.get('topic')
        topic, created   = TopicModel.objects.get_or_create(name = topic_name)
        room.name        = request.POST.get('name')
        room.topic       = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('chat:roomView', pk=room.id)

    f_title = "Edit Room"

    context = {
        "form"    : form,
        "f_title" : f_title,
        "topics"  : topics,
        "room"    : room
    }
    return render(request, 'chat/roomCreateForm.html', context)

@login_required(login_url='chat:loginUser')
def deleteRoom(request, pk):
    room = get_object_or_404(RoomModel, id=pk)

    if request.user != room.host:
        return HttpResponse('Oops! Action not allowed.')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {"obj" : room}
    return render(request, 'chat/delete.html', context)

@login_required(login_url='chat:loginUser')
def deleteMessage(request, pk):
    message = get_object_or_404(MessageModel, id=pk)

    if request.user != message.user:
        return HttpResponse('Oops! Action not allowed.')

    if request.method == 'POST':
        message.delete()
        return redirect('chat:roomView', pk = message.room.id)

    context = {"obj" : message}
    return render(request, 'chat/delete.html', context)

@login_required(login_url='chat:loginUser')
def editUserProfile(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect('chat:userProfileView', uname = user.username)

    context = {
        'form' : form
    }
    return render(request, 'chat/edit-user.html', context)

def topicsView(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = TopicModel.objects.filter(name__icontains = q)
    context = {
        'topics' : topics
    }
    return render(request, 'chat/topicsView.html', context)

def activityView(request):
    msgs = MessageModel.objects.all()[:10]
    context = {
        'msgs' : msgs
    }
    return render(request, 'chat/activityView.html', context)