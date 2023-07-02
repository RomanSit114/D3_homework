from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Post, Author, Category, PostCategory, Comment, News
from django.core.paginator import Paginator
from .filters import NewsFilter
from .forms import NewsForm, CommentForm

class NewsListView(ListView):
    model = Post
    # model = News
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

    # def get(self, request, *args, **kwargs): //написан chatgpt
    #     form = self.form_class()
    #     context = self.get_context_data(**kwargs)
    #     context['form'] = form
    #     return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = self.form_class()  # Добавлено
        # context['categories'] = Category.objects.all()
        return context

    # def post(self, request, *args, **kwargs): код из курсов
    #     form = self.form_class(request.POST)
    #
    #     if form.is_valid():
    #         form.save()
    #
    #     return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news')  # Перенаправление на страницу новостей
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class NewsDetailView(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news-detail', pk=self.kwargs['pk'])  # Перенаправление на страницу с деталями новости
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class SearchListView(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context