from email import message
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def home(request):
    return render(request, "authentic/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists! Please try another username")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered")
            return redirect('home')

        if len(username)>10:
            messages.error(request, "username must be less than 10 characters")

        if pass1 != pass2:
            messages.error(request, "Password Does not match")

        if not username.isalnum():
            messages.error(request, "Username must be Alphanumeric")
            return redirect('home')


        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your Account Has has been successfully created")

        

        return redirect('signin')


    return render(request, "authentic/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentic/index.html", {'fname':fname})

        else:
            messages.error(request, "Bad Credential")
            return redirect('home')

    return render(request, "authentic/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('home')

