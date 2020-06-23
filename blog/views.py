import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import View
from django.http import JsonResponse


# Create your views here.

from userData.models import UserData
from .models import Post
from .forms import NewPost

POSTS_ON_SITE = 20


# class VoteUpPost(View):
def likes(request):
    print(request.body)

    if request.method == "POST":
        post_id = request.POST.get('post_id')
        print(post_id)
        post = Post.objects.get(id=post_id)
        post.likes += 1
        post.save()
        return JsonResponse({'status': True, 'likes': post.likes})

    print(request.body)
    post_id = request.GET.get('post_id')
    print(post_id)
    post = Post.objects.get(id=post_id)

    return JsonResponse({'status': True, 'likes': post.likes})

def make_posts(user):
    if user is None:
        latest_posts = Post.objects.order_by('-pub_date')[:POSTS_ON_SITE]
    else:
        this_user_data = UserData.objects.filter(profile = user)[0]
        latest_posts = Post.objects.filter(author = this_user_data).order_by('-pub_date')[:POSTS_ON_SITE]

    for pst in latest_posts:
        pst.author_id = pst.author.profile.id
        pst.author_name = pst.author.profile.get_username()

    return latest_posts


def home(request):
    latest_posts = make_posts(None)

    template = loader.get_template('blog/index.html')
    context = {
        'latest_posts' : latest_posts,
    }

    return HttpResponse(template.render(context, request))


def user_page(request, user_id):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse('login'))

    user = User.objects.get(id=user_id)

    if user is None:
        return HttpResponseRedirect(reverse('home'))

    latest_posts = make_posts(user)

    return render(request, 'blog/userPage.html', {
        "Users":User,
        "user":request.user,
        "page_owner":user,
        "latest_posts":latest_posts })

def news_feed(request):

    user = request.user

    if user.is_authenticated == False:
        return HttpResponseRedirect(reverse('login'))

    if user is None:
        return HttpResponseRedirect(reverse('login'))

    if request.method == "POST":
        post_form = NewPost(request.POST)

        if post_form.is_valid() == False:
            return HttpResponseRedirect(reverse('home'))

        post = Post()
        post.text = post_form.cleaned_data["text"]
        post.pub_date = datetime.datetime.now()
        post.author = UserData.objects.filter(profile = user)[0]
        post.likes = 0
        post.save()

        return HttpResponseRedirect(reverse('news_feed'))
    else:
        post_form = NewPost()

    latest_posts = make_posts(user)

    return render(request, 'blog/thisUserPage.html', {
        "Users":User,
        "user":user,
        "new_post":post_form,
        "latest_posts":latest_posts })
