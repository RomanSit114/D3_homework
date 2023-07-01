from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Author, Category, PostCategory, Comment
from django.core.paginator import Paginator
from .filters import NewsFilter
from .forms import NewsForm

class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')
    paginate_by = 1
    form_class = NewsForm

    # def get(self, request):
    #     news = Post.objects.all()
    #     p = Paginator(news, 3)
    #
    #     news = p.get_page(request.GET.get('page', 1))
    #
    #     data = {
    #         'news': news,
    #     }
    #     return render(request, 'news.html', data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())

        context['categories'] = Category.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)

class NewsDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context