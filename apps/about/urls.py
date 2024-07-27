from django.urls import path

from apps.about import views

urlpatterns = [
    path(
        "contacts/",
        views.ContactListCreateView.as_view(),
        name="contact-list-create",
    ),
    path(
        "contacts/<int:id>/",
        views.ContactDetailUpdateDestroyView.as_view(),
        name="contact-retrieve-update-destroy",
    ),
    path(
        "socials/",
        views.SocialsListCreateView.as_view(),
        name="social-list-create",
    ),
    path(
        "socials/<int:id>/",
        views.SocialsDetailUpdateDestroyView.as_view(),
        name="social-retrieve-update-destroy",
    ),
    path(
        "services/",
        views.ServiceListCreateView.as_view(),
        name="service-list-create",
    ),
    path(
        "services/<int:id>/",
        views.ServiceDetailUpdateDestroyView.as_view(),
        name="service-retrieve-update-destroy",
    ),
]
