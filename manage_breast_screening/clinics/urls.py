from django.urls import path

from . import views

app_name = "clinics"

urlpatterns = [
    # TODO: we will have something like
    # /clinics/{today,upcoming,completed,all}
    # /clinics/{id}
    path("", views.clinic_list, name="index"),
    path("today/", views.clinic_list, name="index_today", kwargs={"filter": "today"}),
    path(
        "upcoming/",
        views.clinic_list,
        name="index_upcoming",
        kwargs={"filter": "upcoming"},
    ),
    path(
        "completed/",
        views.clinic_list,
        name="index_completed",
        kwargs={"filter": "completed"},
    ),
    path("all/", views.clinic_list, name="index_all", kwargs={"filter": "all"}),
    path("<uuid:id>/", views.clinic, name="show"),
]
