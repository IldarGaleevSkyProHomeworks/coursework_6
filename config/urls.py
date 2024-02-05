"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from django.conf.urls.static import static

from app_blog.models import Article
from config.views import e_handler404, e_handler403

urlpatterns = [
    path('', cache_page(settings.INDEX_PAGE_CACHE_TIME)(TemplateView.as_view(
        template_name='landing/index.html',
        extra_context={
            'popular_articles': Article.objects.order_by('-view_count')[:settings.POPULAR_ARTICLES_COUNT]
        })), name='index'),
    path("captcha/", include('captcha.urls')),
    path("admin/", admin.site.urls),
    path("accounts/", include('app_accounts.urls', namespace='app_accounts')),
    path("mailings/", include('app_mailing.urls', namespace='app_mailings')),
    path('articles/', include('app_blog.urls', namespace='app_blog')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = e_handler404
handler403 = e_handler403

