from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Post
from blog_app import models
from django.contrib import messages
from django.core.mail import send_mail
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email



# Create your views here.
@login_required(login_url='logIn')
def index(request):
    return render(request, 'home.html')

# old sing in 

# def singIn(request):
#     if request.method == 'POST':
#         fname = request.POST.get('fname')
#         lname =request.POST.get('lname')
#         username = request.POST.get('username') 
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         my_user = User.objects.create_user(username,email,password)
#         my_user.save()
#         return redirect('logIn') 
#     return render(request,'singin.html')

# updated sing in validations
def singIn(request):
    if request.method == 'POST':
        fname = request.POST.get('fname', '').strip()
        lname = request.POST.get('lname', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        errors = []

        # First Name
        if not fname:
            errors.append("First name is required.")
        elif not fname.isalpha():
            errors.append("First name must contain only letters.")

        # Last Name
        if not lname:
            errors.append("Last name is required.")
        elif not lname.isalpha():
            errors.append("Last name must contain only letters.")

        # Username
        if not username:
            errors.append("Username is required.")
        elif len(username) < 4:
            errors.append("Username must be at least 4 characters long.")
        elif User.objects.filter(username=username).exists():
            errors.append("Username already exists.")

        # Email
        if not email:
            errors.append("Email is required.")
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors.append("Enter a valid email address.")
            if User.objects.filter(email=email).exists():
                errors.append("Email already registered.")

        # Password
        if not password:
            errors.append("Password is required.")
        elif len(password) < 6:
            errors.append("Password must be at least 6 characters.")
        elif not re.search(r"[A-Z]", password):
            errors.append("Password must contain at least one uppercase letter.")
        elif not re.search(r"[0-9]", password):
            errors.append("Password must contain at least one number.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'singin.html')

        # If all valid, create user
        my_user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=fname,
            last_name=lname
        )
        my_user.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('logIn')

    return render(request, 'singin.html')

def logIn(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
                #  send email to the user
            send_mail(
                    subject='Welcome to Blog Website!',
                    message=(
                        f"Hello {user.username},\n\n"
                        f"Welcome back! You have successfully logged in to the Blog Website.\n"
                        f"We're glad to see you again 😊\n\n"
                        f"Keep writing, reading, and enjoying great content!\n\n"
                        f"Best regards,\n"
                        f"The Blog Website Team"
                    ),
                    from_email='navazdil07@gmail.com',  # your email address
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            return redirect('home')
                #  send email to the user end
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

        # validate if user not fill both field 

        if not title or not content:
            messages.warning(request, "Both title and content are required.")
            return render(request, 'add_post.html')
        
        npost = models.Post(title=title,content=content,author = request.user)
        npost.save()

        messages.success(request, "Post created successfully!")
        return redirect('show_post')
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

def delete_post(request,post_id):

    post = get_object_or_404(Post,id=post_id)
    if post.author == request.user:
        post.delete()
        messages.success(request, "✅ Post deleted successfully.")
    else:
        messages.error(request, "❌ You are not allowed to delete this post.")
    return redirect('show_post')


    