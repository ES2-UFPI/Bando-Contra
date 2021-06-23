"""BandoContra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from .core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/client/detail', views.detailClient, name="detail_client"),
    path('user/partner/detail', views.detailPartner, name="detail_partner"),
    path('', views.temporaryLogin, name="temporary_login"),
    path('user/client/sign_up', views.addClient, name="addClient"),
    path('user/client/edit_profile', views.editClient, name="editClient"),
    path('user/partner/sign_up', views.addPartner, name="addPartner"),
    path('user/partner/edit_profile', views.editPartner, name="editPartner"),
    path('user/partner/schedule', views.detailSchedule, name='detailSchedule')
]
