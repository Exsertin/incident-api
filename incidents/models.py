from django.db import models


class Incident(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        IN_PROGRESS = 'in_progress', 'In Progress'
        RESOLVED = 'resolved', 'Resolved'
        CLOSED = 'closed', 'Closed'

    class Source(models.TextChoices):
        OPERATOR = 'operator', 'Operator'
        MONITORING = 'monitoring', 'Monitoring'
        PARTNER = 'partner', 'Partner'

    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
    )
    source = models.CharField(
        max_length=20,
        choices=Source.choices,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.id}] {self.description[:40]}"
