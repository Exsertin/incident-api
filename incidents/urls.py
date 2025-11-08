from django.urls import path
from .views import IncidentListCreateView, IncidentStatusUpdateView

urlpatterns = [
    path("", IncidentListCreateView.as_view(), name="incident-list-create"),
    path("<int:id>/status", IncidentStatusUpdateView.as_view(), name="incident-update-status"),
]
