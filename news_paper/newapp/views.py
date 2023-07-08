from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import request
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author, Category, PostCategory, Comment, News
from django.core.paginator import Paginator
from .filters import NewsFilter
from .forms import NewsForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse


class NewsListView(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')
    paginate_by = 3
    form_class = NewsForm

    def get(self, request):
        news = Post.objects.all()
        p = Paginator(news, 3)
        news = p.get_page(request.GET.get('page', 1))
        data = {
            'news': news,
        }
        return render(request, 'news.html', data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = self.form_class()
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def post(self, request, *args, **kwargs):
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news')
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)

    # success_url = reverse('news')

    # def get_logout_redirect_url(self):
    #     return self.success_url

@login_required
def i_am_author(request):
   user = request.user
   authors_group = Group.objects.get(name='authors')
   if not request.user.groups.filter(name='authors').exists():
       authors_group.user_set.add(user)
       user.save()
       return redirect('/')
   else:
       return redirect('/')

class NewsDetailView(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news-detail', pk=self.kwargs['pk'])
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)

    def get_success_url(self):
        return reverse('news')

class SearchListView(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context

class NewsCreateView(CreateView):
    form_class = NewsForm
    template_name = 'news_create.html'
    success_url = '/news/'

class NewsUpdateView(LoginRequiredMixin, UpdateView):
    form_class = NewsForm
    template_name = 'news_update.html'
    success_url = '/news/{id}'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class NewsDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    context_object_name = 'new'

