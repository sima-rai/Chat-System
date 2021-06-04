from django.urls import path
from . import views

app_name = "chatapp"

urlpatterns = [
    path("", views.index,  name="index"),
    path("register/", views.register_view, name="register"),
    path("chat/", views.chat_view, name="chats"),
    path('logout/', views.logout_view, name="logout" ),
    
]