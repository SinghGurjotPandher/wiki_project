from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("/<str:title>", views.pullfile, name="content"),
    path("new_entry", views.new_entry, name = "new_entry"),
    path("get_random", views.get_random, name = "get_random"),
    path("get_entry", views.get_entry, name = "get_entry"),
    path("edit_page", views.edit_page, name = "edit_page"),
    path("save_changes", views.save_changes, name = "save_changes")
]
