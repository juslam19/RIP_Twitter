import json
from django.urls import reverse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

from .models import User, Post, Like, Follow

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "network/register.html")

def index(request):
    if request.method == "POST":
        user = request.user
        post = request.POST.get("post")
        timestamp = datetime.now()
        Post.objects.create(user = user, post = post, timestamp = timestamp, likes = 0)

    current_page = pageify(request, Post.objects.all().order_by('-timestamp'))

    return render(request, "network/index.html", {
        "posts": current_page
    })

def following(request):
    user = request.user
    following = Follow.objects.filter(follower=request.user).values('following_id')

    current_page = pageify(request, Post.objects.filter(user__in=following).order_by('-timestamp'))

    return render(request, "network/following.html", {
        "posts": current_page
    })

def profile(request, owner):
    owner = User.objects.get(id=owner)
    button = None

    user_follow = Follow.objects.filter(follower=request.user, following=owner).count() != 0
    if user_follow:
        button = "Unfollow"
    else:
        button = "Follow"

    if request.method == "POST":
        if request.POST.get("button") == "Follow":
            button = "Unfollow"
            Follow.objects.create(follower=request.user, following=owner)
        else:
            button = "Follow"
            Follow.objects.get(follower=request.user, following=owner).delete()

    current_page = pageify(request, Post.objects.filter(user=owner.id).order_by('-timestamp'))

    return render(request, "network/profile.html", {
        "owner": owner,
        "posts": current_page,
        "followers": Follow.objects.filter(following=owner).count(),
        "following": Follow.objects.filter(follower=owner).count(),
        "button": button
})

@csrf_exempt
def like(request, post_id):

    if request.method == "PUT":
        uniqueLike = Like.objects.filter(user=request.user, post=Post.objects.get(id=post_id)).count()
        if json.loads(request.body).get("like"):
            if uniqueLike == 0:
                Like.objects.create(user=request.user, post=Post.objects.get(id=post_id))
        else:
            if uniqueLike == 1:
                Like.objects.filter(user=request.user, post=Post.objects.get(id=post_id)).delete()

        post = Post.objects.get(id=post_id)
        post.likes = Like.objects.filter(post=post).count()
        post.save()

    if request.method == "GET":
        return JsonResponse(Post.objects.get(id=post_id).serialize())

@csrf_exempt
def like_helper(request, post_id):
    if request.method == "GET":
        like_count = Like.objects.filter(user=request.user, post=Post.objects.get(id=post_id)).count()
        if (like_count == 0) :
            return JsonResponse({ 'message':'error' })
        elif (like_count == 1):
            return JsonResponse({ 'message':'success' })
        else:
            # DO NOTHING
            # For error checking ONLY
            return JsonResponse({ 'message':'SNAFU' })

@csrf_exempt
def edit(request, post_id):

    if request.method == "PUT":
        post = Post.objects.get(id=post_id)
        post.post = json.loads(request.body).get("post")
        post.save()

@csrf_exempt
def pageify(request, posts):
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    current_page = paginator.get_page(page_number)
    return current_page