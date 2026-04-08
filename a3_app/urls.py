from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('products/', views.products, name='products'),
    path('contact/', views.contact, name='contact'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/mark-read/<int:pk>/', views.mark_read, name='mark_read'),
    path('dashboard/delete/<int:pk>/', views.delete_contact, name='delete_contact'),
    path('dashboard/login/', auth_views.LoginView.as_view(template_name='dashboard_login.html'), name='login'),
    path('dashboard/logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
]
