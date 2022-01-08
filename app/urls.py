from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('city/', views.city, name='city'),
    path('delete/<city_name>/', views.delete_city, name='delete_city'),
    path('home/',views.index,name='home'),
    path('register/', views.register, name='register'),
    path('', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='prof'),
    path('prof/', views.prof, name='profile'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
