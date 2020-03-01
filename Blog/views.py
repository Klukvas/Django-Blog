from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.http import  HttpResponseRedirect




from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_Post(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # get details of a single Post
    if request.method == 'GET':
        # posts = Post.objects.all()
        # serializer = PostSerializer(posts, many=True)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    # delete a single Post
    elif request.method == 'DELETE':
        return Response({})
    # update details of a single Post
    elif request.method == 'PUT':
        return Response({})
@api_view(['GET', 'POST'])
def get_post_puppies(request):
    # get all puppies
    if request.method == 'GET':
        return Response({})
    # insert a new record for a Post
    elif request.method == 'POST':
        return Response({})


class DeleteNewsView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'Blog/post_confim_delete.html'
    def test_func(self):
        news = self.get_object()
        if self.request.user == news.autor:
            return True
        return False


def home(request):
    data = {
        'news': Post.objects.all(),
        'title': 'Главная страница блога'
    }
    return render(request, 'Blog/home.html', data)


class ShowNewView(ListView):
    model = Post
    template_name = 'Blog/home.html'
    context_object_name = 'news'
    ordering = ['-date']
    paginate_by = 5
    def get_context_data(self, **kwards):
        ctx = super(ShowNewView, self).get_context_data(**kwards)
        ctx['title'] = 'Главная страница блога'

        return ctx


class UserAllNewsView(ListView):
    model = Post
    template_name = 'Blog/user_news.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(autor=user).order_by('-date')


    def get_context_data(self, **kwards):
        ctx = super(UserAllNewsView, self).get_context_data(**kwards)
        ctx['title'] = f'All posts from {self.kwargs.get("username")}'

        return ctx


def NewsDetailView(request, id):
    post = get_object_or_404(Post, id=id)
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    context={
        'post': post,
        'is_liked': is_liked,
        'total_likes':post.total_likes()
    }        
      

    return render(request,'Blog/news_detail.html', context )


def contacti(request):
    return render(request, 'Blog/contact.html', {'title':'Link us for free'})


class CreateNewsView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


class UpdateNewsView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        news=self.get_object()
        if self.request.user == news.autor:
            return True
        return False
    
def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(post.get_absolute_url())

# def dislike_post(request):
#     post = get_object_or_404(Post, id=request.POST.get('post_id'))
#     post.dislikes.add(request.user)
#     return HttpResponseRedirect(post.get_absolute_url())
