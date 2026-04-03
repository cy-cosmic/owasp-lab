from django.urls import path

from polls import views

urlpatterns = [
    path("", views.index, name="mainindex"),
    path("secure/polls", views.polls, name="polls"),
    path("secure/polls/<int:poll_id>/detail/", views.detail, name="detail"),
    path("secure/polls/<int:poll_id>/results/", views.results, name="results"),
    path("secure/polls/<int:poll_id>/vote/", views.vote, name="vote"),
]
