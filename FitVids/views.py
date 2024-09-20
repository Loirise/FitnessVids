from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import VideoModel
from .forms import VideoForm, UserSignUpForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.hashers import make_password



def FrontPageView(request):
    
    if request.method == "GET":
        return render(request, "frontpage.html")


def VideoListView(request):

    if request.method == "GET":
        if request.user.is_authenticated and request.user.has_perm('FitVids.view_videomodel'):
            posts = VideoModel.objects.all()
            return render(request, "videos_list.html", {'posts': posts})
        else:
            return redirect("frontpage")


def VideoUploadView(request):

    if request.user.is_authenticated and request.user.has_perm('FitVids.add_videomodel'):
        if request.method == 'POST':
            form = VideoForm(request.POST, request.FILES)
            if form.is_valid():
                instance = VideoModel(title=request.POST.get('title'), video=request.FILES.get('file'))
                instance.save()
                return HttpResponseRedirect(reverse_lazy('video_list'))
        else:
            form = VideoForm()
        return render(request, "upload.html", {'form':form})
    return redirect("video_list")


def UserSignUpView(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user_instance = User(
                username = request.POST.get('username'),
                password = make_password(request.POST.get('password')),
                email = request.POST.get('email'),
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name')
            )
            user_instance.save()
            group = Group.objects.get(name="User")
            user_instance.groups.add(group)
            permission = Permission.objects.get(codename="view_videomodel")
            user_instance.user_permissions.add(permission)
            login(request, user_instance)
            return HttpResponseRedirect(reverse_lazy('video_list'))
    else:
        if request.user.is_authenticated:
            return redirect("frontpage")
        form = UserSignUpForm()
    return render(request, "auth/sign_up.html", {'form': form})


def UserLoginView(request): 

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse_lazy('frontpage'))
            else:
                return HttpResponseRedirect(reverse_lazy('login_page'))
    else:
        if request.user.is_authenticated:
            return redirect("frontpage")
        form = UserLoginForm()
    return render(request, "auth/login.html", {'form': form})


def UserLogoutView(request):
    if request.method == "POST":
        logout(request)
        return HttpResponseRedirect(reverse_lazy('frontpage'))
    return render(request, "auth/logout.html")