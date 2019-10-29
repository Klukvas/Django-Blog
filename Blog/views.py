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

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class DeleteNewsView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/post_confim_delete.html'
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
    return render(request, 'blog/home.html', data)



class ShowNewView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'news'
    ordering = ['-date']
    paginate_by = 5
    def get_context_data(self, **kwards):
        ctx = super(ShowNewView, self).get_context_data(**kwards)
        ctx['title'] = 'Главная страница блога'

        return ctx


class UserAllNewsView(ListView):
    model = Post
    template_name = 'blog/user_news.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(autor=user).order_by('-date')


    def get_context_data(self, **kwards):
        ctx = super(UserAllNewsView, self).get_context_data(**kwards)
        ctx['title'] = f'All posts from {self.kwargs.get("username")}'

        return ctx


class NewsDetailView(DetailView):
    template_name = 'blog/news_detail.html'
    model = Post
    def get_context_data(self, **kwards):
        ctx = super(NewsDetailView, self).get_context_data(**kwards)
        ctx['title'] = Post.objects.filter(pk=self.kwargs['pk']).first()

        return ctx


def contacti(request):
    return render(request, 'blog/contact.html', {'title':'Link us for free'})


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