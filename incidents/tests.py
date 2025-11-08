from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status, exceptions
from .serializers import IncidentSerializer
from .models import Incident

# MARK: - Module Tests

class IncidentModelTests(TestCase):

    def test_default_status_is_open(self):
        # given
        # ...
        # when
        inc = Incident.objects.create(description="Test", source=Incident.Source.OPERATOR)
        # then
        self.assertEqual(inc.status, Incident.Status.OPEN)

# MARK: - API Tests

class IncidentAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.base_url = "/api/incidents/"

    def test_create_incident(self):
        # given
        data = {"description": "Самокат не в сети", "source": Incident.Source.MONITORING}
        # when
        response = self.client.post(self.base_url, data, format="json")
        # then
        model = __response_to_model__(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(model.description, data["description"])
        self.assertEqual(model.source, data["source"])
        self.assertEqual(model.status, Incident.Status.OPEN)

    def test_list_incidents_filter_by_status(self):
        # given
        Incident.objects.create(description="A", source=Incident.Source.OPERATOR, status=Incident.Status.OPEN)
        Incident.objects.create(description="B", source=Incident.Source.OPERATOR, status=Incident.Status.RESOLVED)
        test_status = Incident.Status.OPEN
        # when
        response = self.client.get(self.base_url + "?status=" + test_status)
        count = Incident.objects.filter(status=test_status).count()
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, 1)

    def test_update_status_success(self):
        # given
        inc = Incident.objects.create(description="отчёт не выгрузился", source=Incident.Source.PARTNER)
        url = f"{self.base_url}{inc.id}/status"
        # when
        response = self.client.patch(url, {"status": Incident.Status.RESOLVED}, format="json")
        response_data = response.json()
        model = __response_to_model__(response)
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["id"], inc.id)
        self.assertEqual(model.status, Incident.Status.RESOLVED)
        inc.refresh_from_db()
        self.assertEqual(inc.status, Incident.Status.RESOLVED)

    def test_update_no_valid_status(self):
        # given
        inc = Incident.objects.create(description="To be resolved", source=Incident.Source.PARTNER)
        url = f"{self.base_url}{inc.id}/status"
        new_status = 1
        # when
        response = self.client.patch(url, {"status": new_status}, format="json")
        response_data = response.json()
        # then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data["status"][0], f'"{new_status}" is not a valid choice.')
        inc.refresh_from_db()
        self.assertNotEqual(inc.status, new_status)

    def test_update_status_not_found_returns_404(self):
        # given
        url = f"{self.base_url}9999/status/"
        # when
        resp = self.client.patch(url, {"status": Incident.Status.RESOLVED}, format="json")
        #then
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

# MARK: - Private

def __response_to_model__(response) -> Incident:
    data = response.json()
    serializer = IncidentSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return Incident(**serializer.validated_data)