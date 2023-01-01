from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import DiarySubmission, User
from django.db import IntegrityError
from .forms import PartialSubmissionForm

# Create your views here.

# Register Functionality
def register(request):

    # Facilitate POST request method
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "soleapp/register.html", {
                "message": "Passwords do not match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "soleapp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "soleapp/register.html")

# Login Functionality
def loginClient(request):
    # Facilitate POST request
    if request.method == 'POST':
        # Access submitted data
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate data
        client = authenticate(request, username=username, password=password)

        # Inspect whether authentication is successful
        if client is not None:
            login(request, client)
            # Redirect to index
            return HttpResponseRedirect(reverse('index'))
        else:
            context = {
                'message': 'Invalid log in credentials.'
            }
            return render(request, "soleapp/login.html", context)

    return render(request, "soleapp/login.html")



# Logout Functionality
def logoutClient(request):
    logout(request)
    # Redirect to login page
    return HttpResponseRedirect(reverse('login'))


# Homepage Functionality
# Limit url route to logged in users only
@login_required(login_url="login")
def homePage(request):

    # Facilitate the making of new DiarySubmissions
    if request.method == 'POST':
        # Provide unpopulated values
        partialInstance = DiarySubmission(creator=request.user)
        # Populate PartialsubmissionForm with POST data
        form = PartialSubmissionForm(request.POST, instance=partialInstance)

        # Form validation
        if form.is_valid:
            # Save Model object into the database
            form.save()
        else:
            # Access all of user's posts
            posts = DiarySubmission(creator=request.user)
            # Send bound form instance back to the User, Django will provide error messages
            context = {
                'form': form,
                'posts': posts
            }
            return render(request, "soleapp/index.html", context)

    # Access User model object
    # Access appropiate Post model object instances
    posts = DiarySubmission.objects.filter(creator=request.user)
    # Form
    form = PartialSubmissionForm
    # Send info via context (data type: dictionary)
    context = {
        'posts': posts,
        'form': form
    }

    # Redirect user to index page
    return render(request, "soleapp/index.html", context)