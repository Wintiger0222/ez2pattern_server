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
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('ez2on.urls')),
    path('djmax/', include('djmax.urls')),

    path('robots.txt/', TemplateView.as_view(template_name="robots.txt", 
         content_type='text/plain')),
]

# if settings.DEBUG is False:
#     urlpatterns += [
#         re_path(r'^{{본인 media_url 값}}/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}), # 나는 uploads
#         re_path(r'^{{본인 static_url 값}}/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}) # 나는 static
#     ]
