from django.db import models


class Location(models.Model):
    city_name = models.CharField(max_length=100)
    population = models.IntegerField()


class Subscription(models.Model):
    email = models.EmailField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    confirmation_id = models.UUIDField(null=True)
    confirmation_requested_at = models.DateTimeField(null=True)
    subscribed = models.BooleanField(default=False)
    subscribed_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    unsubscribed_at = models.DateTimeField(null=True)
