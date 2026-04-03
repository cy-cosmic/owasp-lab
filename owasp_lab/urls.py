from django.urls import path, include




urlpatterns = [
    path("", include("polls.urls")),
    path("labs/", include("labs.urls")),
]
