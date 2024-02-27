from django.urls import path
from article import views

urlpatterns = [
    path('all', views.ArticleListView.as_view(), name='article_list'),
    path('article_detail/<slug:slug>', views.ArticleDetailView.as_view(), name='article_detail'),
]
