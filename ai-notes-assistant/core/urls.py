from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("materials/", views.material_list, name="material_list"),
    path("materials/upload/", views.material_upload, name="material_upload"),
    path(
        "materials/<int:material_id>/open/",
        views.material_open,
        name="material_open",
    ),
    path(
        "materials/<int:material_id>/delete/",
        views.material_delete,
        name="material_delete",
    ),
]