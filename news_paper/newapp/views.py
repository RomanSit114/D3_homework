from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import request
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author, Category, PostCategory, Comment, News, CategorySubscriber
from django.core.paginator import Paginator
from .filters import NewsFilter
from .forms import NewsForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

class NewsListView(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')
    paginate_by = 3
    form_class = NewsForm

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

@login_required
def i_am_author(request):
   user = request.user
   authors_group = Group.objects.get(name='authors')
   if not request.user.groups.filter(name='authors').exists():
       authors_group.user_set.add(user)
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

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'cat.html'
    context_object_name = 'cat'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(id=self.kwargs['pk'])
        context['subscribers'] = category.subscribers.all()
        return context

class SearchListView(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context

class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('newapp.add_post')
    form_class = NewsForm
    template_name = 'news_create.html'
    success_url = '/news/'

    # функция, которая уведомляет на почту подписчиком данной категории новостей
    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)

        self.object = form.save()

        self.postCategory_list = self.object.postCategory.all()

        for category in self.postCategory_list:

            for sub in category.subscribers.all():

                html_content = render_to_string(
                    'send_mail_subscribe_to_news.html',
                    {
                        'user': sub,
                        'post': self.object,
                    }
                )

                msg = EmailMultiAlternatives(
                    subject=f'{self.object.title}',
                    body=self.object.text,
                    from_email='roma.sitdikov@yandex.ru',
                    to=[f'{sub.email}'],
                )
                msg.attach_alternative(html_content, "text/html")  # добавляем html
                msg.send()  # отсылаем

        return HttpResponseRedirect(self.get_success_url())


class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('newapp.change_post')
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

def subscribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.add(request.user.id)
    return HttpResponseRedirect(reverse('cat', args=[pk]))

def unsubscribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.remove(request.user.id)
    return HttpResponseRedirect(reverse('cat', args=[pk]))
