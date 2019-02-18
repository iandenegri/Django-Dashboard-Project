"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path

from news.views import scrape, news_list

from finance.views import company_article_list, ChartData, dash, dash_ajax

from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="dashboard"),
    path('notepad/', include(("notepad.urls", "notepad"), namespace='notepad')),
    path('scrape/', scrape, name="scrape"),
    path('news_home/', news_list, name="news_home"),
    path('companies/', company_article_list, name='companies'),
    # Two paths below need to be reg expressions to work with dashly.
    re_path('^_dash-', dash_ajax),
    re_path('^dash', dash),
    
    path('api/chart/data', ChartData.as_view(), name='api-chart-data'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
