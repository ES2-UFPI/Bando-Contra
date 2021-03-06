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
from django.urls import path, include
from .core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('user/client/detail', views.detailClient, name="detail_client"),
    path('user/partner/detail', views.detailPartner, name="detail_partner"),
    path('', views.home, name="home"),
    path('login/temporary', views.temporaryLogin, name="temporary_login"), #Apagar depois de fazer a tela de login
    path('user/client/sign_up', views.addClient, name="addClient"),
    path('user/client/edit_profile', views.editClient, name="editClient"),
    path('user/client/add_service', views.addService, name="addService"),
    path('user/partner/edit_service/<int:pk>', views.editService, name="editService"),
    path('user/partner/sign_up', views.addPartner, name="addPartner"),
    path('user/partner/edit_profile', views.editPartner, name="editPartner"),
    path('user/partner/schedule', views.detailSchedule, name='detailSchedule'),
    path('user/partner/add_event', views.addEvent, name='addEvent'),
    path('user/partner/edit_event/<int:pk>', views.editEvent, name='editEvent'),
    path('user/partner/delete_event/<int:pk>', views.deleteEvent, name='deleteEvent'),
    path('user/detail_service/<int:pk>', views.detailService, name='detailService'),
    path('user/client/list_services/', views.listClientServices, name='listClientServices'),
    path('user/partner/list_services/', views.listPartnerServices, name='listPartnerServices'),
    path('testLogin/<str:username>', views.testLogin),
    path('user/client/feedback/<int:pk>', views.feedback, name='feedback')
]
