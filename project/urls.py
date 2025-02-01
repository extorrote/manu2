"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from manuelapp import views
from django.conf import settings
from django.conf.urls.static import static






urlpatterns = [
    path('admin/', admin.site.urls),
    path('list_condos/' , views.index, name="list_condos"),
    path('', views.index, name='index'),
    path('about_us/', views.about_us, name='about_us'),
    path('property_management/', views.property_management, name="property_management"),
    path('private_chef/' , views.private_chef, name="private_chef"),
    path('send_email/' , views.send_email, name="send_email"),
    path('contact/' , views.contact, name="contact"),

    path('login/',views.login_user,name="login"),
    path('logout/',views.logout_user,name="logout"),
     
    path('condos/<int:condo_id>/', views.condo_detail, name='condo_detail'),#ESTE ES EL QUE ME DA EL LINK SEPARADO DE CADA CONDO
    path('post_condo/', views.post_condo, name='post_condo'),
    path('reserve/<int:condo_id>/', views.condo_calendar_and_reserve, name='reserve_condo'),
    path('check-availability/', views.check_date_availability, name='check_availability'),
    path('terms_and_conditions/', views.terms_and_conditions,name="terms_and_conditions"),
    path('send_email/',views.send_email,name="send_email"),
    path('terms_and_conditions/' , views.terms_and_conditions, name="terms_and_conditions"),
    path('privacy_policy/',views.privacy_policy, name="privacy_policy")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
