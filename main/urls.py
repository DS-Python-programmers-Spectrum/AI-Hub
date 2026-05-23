from django.urls import path

from . import views

from django.contrib.auth import views as auth_views


urlpatterns = [

    # Home Page
    path('', views.home, name='home'),

    # AI Features
    path('chatbot/', views.chatbot, name='chatbot'),

    path('generate-image/', views.generate_image,
         name='generate_image'),

    path('generate-code/', views.generate_code,
         name='generate_code'),

    # Authentication
    path('signup/', views.signup_view,
         name='signup'),

    path(
        'login/',

        auth_views.LoginView.as_view(
            template_name='login.html'
        ),

        name='login'
    ),

    path(
        'logout/',

        auth_views.LogoutView.as_view(),

        name='logout'
    ),

    # Dashboard
    path('dashboard/', views.dashboard,
         name='dashboard'),

]