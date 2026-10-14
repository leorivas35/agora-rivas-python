from django.urls import path

from agora_rivas.interfaces.api import views

urlpatterns = [
    path("health", views.health, name="health"),
    path("users", views.create_user, name="create-user"),
]
