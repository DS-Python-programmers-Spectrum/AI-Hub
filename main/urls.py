from django.urls import path
from . import views


urlpatterns = [

    path('',views.home,name='home'),
        path('chatbot/',views.chatbot),
        path('generate-image/', views.generate_image),
        path('generate-code/', views.generate_code),

]