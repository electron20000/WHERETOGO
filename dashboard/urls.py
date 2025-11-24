from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("fragment/", views.dashboard_fragment, name="dashboard_fragment"),
    path("leader/", views.leader_panel, name="leader_panel"),
    path("appearance-preview/", views.appearance_preview, name="appearance_preview"),
]
