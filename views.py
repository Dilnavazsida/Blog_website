from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Post
from . import models

# Create your views here.
@login_required(login_url='logIn')
def index(request):
    return render(request, 'home.html')

def singIn(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname =request.POST.get('lname')
        username = request.POST.get('username') 
        email = request.POST.get('email')
        password = request.POST.get('password')
        my_user = User.objects.create_user(username,email,password)
        my_user.save()
        return redirect('logIn') 
    return render(request,'singin.html')

def logIn(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return redirect("logIn")
    return render(request,'login.html')

def logOut(request):
    logout(request)
    return redirect('singIn')

def show_post(request):
    posts = Post.objects.all()
    return render(request,'show_post.html',{'posts':posts})

def add_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        npost = models.Post(title=title,content=content,author = request.user)
        npost.save()
        return redirect('home')
    return render(request,'add_post.html')


def my_post(request):
    context = {'posts':Post.objects.filter(author = request.user)}
    return render(request,'mypost.html',context)

@login_required
def edit_post(request,post_id):

    post = get_object_or_404(Post,id=post_id)

    # only allow the owner to edit 

    if post.author != request.user:
        return redirect('home')
    
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('my_post')

    return render(request, 'edit_post.html', {'post': post})

def search_post(request):
    query = request.GET['query']
    if len(query)>50:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request,"No search result found please refine your search")
    return render(request,'search_post.html',{'posts':allPosts,'query':query})

