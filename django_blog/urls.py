from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from article.views import HomePageView
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path("robots.txt",
         TemplateView.as_view(template_name="robots.txt",
                              content_type="text/plain")
         ),
]

urlpatterns += i18n_patterns(
    path('', HomePageView.as_view(), name='home'),
    path('article/', include(('article.urls', 'article'), namespace='article')),
    path('i18n/', include('django.conf.urls.i18n')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)