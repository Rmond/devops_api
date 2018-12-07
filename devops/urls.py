"""devops URL Configuration

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
import xadmin
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from assets.views import *
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token


router = DefaultRouter()

router.register(r'user', UserViewset, base_name="user")
router.register(r'host', HostViewset, base_name="host")

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
    url(r'^login/', obtain_jwt_token),
    url(r'^refresh/', refresh_jwt_token),
    url(r'docs/', include_docs_urls(title="韩都衣舍")),
]
