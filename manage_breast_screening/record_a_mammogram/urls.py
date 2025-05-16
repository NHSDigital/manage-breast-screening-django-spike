from django.urls import path

from . import views

app_name = "record_a_mammogram"

urlpatterns = [
    path(
        "appointments/<int:id>/check-in/",
        views.check_in,
        name="check_in",
    ),
    path(
        "appointments/<int:id>/start-screening/",
        views.StartScreening.as_view(),
        name="start_screening",
    ),
    path(
        "appointments/<int:id>/ask-for-medical-information/",
        views.AskForMedicalInformation.as_view(),
        name="ask_for_medical_information",
    ),
    path(
        "appointments/<int:id>/record-medical-information/",
        views.RecordMedicalInformation.as_view(),
        name="record_medical_information",
    ),
    path(
        "appointments/<int:id>/awaiting-images/",
        views.awaiting_images,
        name="awaiting_images",
    ),
    path(
        "appointments/<int:id>/cannot-go-ahead/",
        views.appointment_cannot_go_ahead,
        name="appointment_cannot_go_ahead",
    ),
]
