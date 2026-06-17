from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .forms import RegisterForm, PostForm, CommentForm
from .models import Post, Comment, Like, Follow


def home(request):
    posts = Post.objects.all().order_by('-created_at')

    return render(
        request,
        'socialapp/home.html',
        {
            'posts': posts,
            'user': request.user
        }
    )


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/login/')

    else:
        form = RegisterForm()

    return render(
        request,
        'socialapp/register.html',
        {'form': form}
    )


def user_login(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('/')

    return render(request, 'socialapp/login.html')


def create_post(request):

    if request.method == 'POST':

        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            return redirect('/')

    else:
        form = PostForm()

    return render(
        request,
        'socialapp/create_post.html',
        {'form': form}
    )


def add_comment(request, post_id):

    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()

    return redirect('/')


def like_post(request, post_id):

    post = Post.objects.get(id=post_id)

    Like.objects.get_or_create(
        post=post,
        user=request.user
    )

    return redirect('/')


def follow_user(request, user_id):

    user_to_follow = User.objects.get(id=user_id)

    if request.user != user_to_follow:
        Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

    return redirect('/')