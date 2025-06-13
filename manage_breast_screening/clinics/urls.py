from django.urls import path

from . import views

app_name = "clinics"

urlpatterns = [
    # Clinic list
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
    # Clinic show
    path("<uuid:id>/", views.clinic, name="show"),
    path(
        "<uuid:id>/remaining/",
        views.clinic,
        name="show_remaining",
        kwargs={"filter": "remaining"},
    ),
    path(
        "<uuid:id>/checked_in/",
        views.clinic,
        name="show_checked_in",
        kwargs={"filter": "checked_in"},
    ),
    path(
        "<uuid:id>/complete/",
        views.clinic,
        name="show_complete",
        kwargs={"filter": "complete"},
    ),
    path("<uuid:id>/all/", views.clinic, name="show_all", kwargs={"filter": "all"}),
    path(
        "<uuid:id>/appointment/<uuid:appointment_id>/check-in/",
        views.check_in,
        name="check_in",
    ),
]
