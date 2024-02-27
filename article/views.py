from django.views.generic import (
    ListView,
    TemplateView,
    DetailView,
)
from article.models import Article
from view_breadcrumbs import (
    ListBreadcrumbMixin,
    DetailBreadcrumbMixin,
)
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(TemplateView):
    template_name = 'home.html'


class ArticleListView(LoginRequiredMixin, ListBreadcrumbMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(status='pu').order_by('-created_at')


class ArticleDetailView(LoginRequiredMixin, DetailBreadcrumbMixin, DetailView):
    model = Article
    breadcrumb_use_pk = False
    template_name = 'article_detail.html'
    count_hit = True

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        obj.viewed()
        self.object = obj
        return obj