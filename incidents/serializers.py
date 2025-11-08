from rest_framework import serializers
from .models import Incident


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = "__all__"

class IncidentStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'
        read_only_fields = ['description', 'source']
        extra_kwargs = {"status": {"required": True}}
