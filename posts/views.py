from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Post, Like
from profiles.models import Profile
from .forms import PostModelForm
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
import requests
from django.contrib.auth.models import auth, User

# @login_required
def list_view(request):
    qs = Post.objects.all().order_by('created')
    paginator = Paginator(qs, 6)
    page_number = request.GET.get('page')
    qsfinal = paginator.get_page(page_number)
    total_pages = qsfinal.paginator.num_pages

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
    else:
        profile = None
    context = {
        'qs': qsfinal,
        'profile': profile,
        'lastpage': total_pages,
        'totalPageList': [n+1 for n in range(total_pages)]
    }

    return render(request, 'posts/main.html', context)

@login_required
def post_create(request):
    qs = Post.objects.all()
    profile = Profile.objects.get(user=request.user)
    post_added = False

    if request.method == 'POST':
        # print(request.FILES)
        data = request.POST
        dataImage = request.FILES
        title = data['title']
        link = data['link']
        description = data['description']
        image = dataImage['picture']
        p_form = Post(title=title,content=description,link=link,image=image,author=profile)
        p_form.save()
        p_form = PostModelForm()
        post_added = True

    context = {
        'qs': qs,
        'profile': profile,
        'post_added': post_added,
    }

    return render(request, 'posts/addposts.html', context)

@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created: # created is a bool, if already that Like object is there, created = false(i.e we haven't created, just GET that Like object)
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'

        post_obj.save()
        like.save()

        return redirect('posts:main-post-view')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('posts:main-post-view')
    # success_url = '/posts/'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You need to be the author of the post in order to delete it')
        return obj

class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostModelForm
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:main-post-view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "You need to be the author of the post in order to update it")
            return super().form_invalid(form)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        url = "https://backend.credenz.in/api/check_user/"
        payload={'username': username,
                'password': password,
                'event': 'Webweaver'
                }
        response = requests.request("POST", url, data=payload)
        if response.status_code == 200:
            data = response.json()
            print(data)
            print("Senior : ",data['senior'])
            print("Bool Check : ",bool(User.objects.filter(username=username).exists()))
            if not(User.objects.filter(username=username).exists()):
                user = User.objects.create_user(username=username, password=password, email="dummy@gmail.com", first_name="dummyfname", last_name="dummylname")
                user.save()
        else:
            url = "https://registrations.credenz.in/api/event_players/check_user/"
            payload={'username': username,
                    'password': password,
                    'event': 'Web Weaver'
                }
            response = requests.request("POST", url, data=payload)
            if response.status_code == 200:
                data = response.json()
                print("Senior : ",data['senior'])
                print("Bool Check : ",bool(User.objects.filter(username=username).exists()))
                if not(User.objects.filter(username=username).exists()):
                    user = User.objects.create_user(username=username, password=password, email="dummy@gmail.com", first_name="dummyfname", last_name="dummylname")
                    user.save()
            else:
                # messages.error(request,"User does exist")
                # return render(request, 'posts/login.html', {'title': 'Login'})
                return render(request, 'posts/login.html', context={'data': {
                'message': 'Users does not exist'
            }})
        # print('Username : {}\nPassword : {}'.format(username, password))
        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'posts/login.html', context={'data': {
                'message': 'Wrong Credentials'
            }})
    elif request.method == 'GET':
        return render(request, 'posts/login.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def web_team(request):
    return render(request, 'posts/webteam.html')