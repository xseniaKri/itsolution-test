"""
URL configuration for quotes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import urls
from django.urls import include, path
from django.views.generic import RedirectView

from quotesapp.views import profile, register

urlpatterns = [
    path("admin/", admin.site.urls),
    path("quotesapp/", include("quotesapp.urls")),
    path("", RedirectView.as_view(url="/quotesapp/", permanent=True)),
    path("accounts/", include(urls)),
    path("accounts/register/", register, name="register"),
    path("accounts/profile/", profile, name="profile"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
