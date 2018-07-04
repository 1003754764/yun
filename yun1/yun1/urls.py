"""yun1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
# from django.contrib import admin

from django.views import static
from django.conf import settings


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^ueditor/', include('ueditor.urls')),
    url(r'^myadmin/', include('myadmin.urls')),
    url(r'^', include('myhome.urls')),

     # 增加以下一行，以识别静态资源
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static')

]
