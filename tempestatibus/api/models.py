import uuid
from django.db import models

class Location(models.Model):
	city_name = models.CharField(max_length=100)
	population = models.IntegerField()

class Subscription(models.Model):
	email = models.EmailField()
	location = models.ForeignKey(Location, on_delete=models.CASCADE)
	confirmation_id = models.UUIDField(default=uuid.uuid4)
	confirmation_requested_at = models.DateTimeField()
	subscribed = models.BooleanField(default=False)
	subscribed_at = models.DateTimeField(null=True)

