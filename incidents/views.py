from rest_framework import generics
from .models import Incident
from .serializers import IncidentSerializer, IncidentStatusUpdateSerializer


class IncidentListCreateView(generics.ListCreateAPIView):
    queryset = Incident.objects.all().order_by("-created_at")
    serializer_class = IncidentSerializer

    def get_queryset(self):
        status_param = self.request.query_params.get("status")

        if status_param:
            return self.queryset.filter(status=status_param)

        return self.queryset.all()


class IncidentStatusUpdateView(generics.UpdateAPIView):
    queryset = Incident
    serializer_class = IncidentStatusUpdateSerializer
    lookup_field = "id"
