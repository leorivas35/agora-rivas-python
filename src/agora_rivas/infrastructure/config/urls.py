from django.urls import include, path

urlpatterns = [
    path("api/", include("agora_rivas.interfaces.api.urls")),
]
