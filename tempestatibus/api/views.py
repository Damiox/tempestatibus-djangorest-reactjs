import re, json
from datetime import timedelta
from django.utils import timezone
from rest_framework import viewsets, views, generics, exceptions
from rest_framework.response import Response
from tempestatibus.api.models import Subscription, Location
from tempestatibus.api.serializers import LocationSerializer

class LocationView(generics.GenericAPIView):
    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

class ConfirmSubscriptionView(generics.GenericAPIView):
    def post(self, request, *args, **kwarg):
        confirmation_id = kwarg.get('confirmation_id')
        try:
            subscription = Subscription.objects.get(confirmation_id=confirmation_id)
        except Subscription.DoesNotExist:
            raise exceptions.ParseError(detail="ConfirmationId is invalid")
        if subscription.subscribed is True:
            raise exceptions.ParseError(detail="Subscription was already confirmed")
        if self.is_confirmation_expired(subscription):
            raise exceptions.ParseError(detail="ConfirmationId is expired")
        subscription.subscribed = True
        subscription.subscribed_at = timezone.now()
        subscription.save()
        return Response()
    def is_confirmation_expired(self, subscription):
        now = timezone.now()
        requested_at = subscription.confirmation_requested_at
        return now - requested_at > timedelta(hours=24)

class SubscribeReceiptView(generics.GenericAPIView):
    def post(self, request, *args, **kwarg):
        # Parsing request body
        body = json.loads(request.body.decode('utf-8'))
        
        # Validating body
        if 'email' not in body:
            raise exceptions.ParseError(detail="email is missing")
        if 'city_name' not in body:
            raise exceptions.ParseError(detail="city_name is missing")

        email = body['email']
        city_name = body['city_name']

        if not re.compile(r"[^@]+@[^@]+\.[^@]+").match(email):
            raise exceptions.ParseError(detail="email is invalid")
        
        try:
            location = Location.objects.get(city_name=city_name)
        except Location.DoesNotExist:
            raise exceptions.ParseError(detail="City Invalid")
        # Completed validating body

        try:
            subscription = Subscription.objects.get(email=email)
            if subscription.subscribed is True:
                raise exceptions.ParseError(detail="Email is already subscribed")
        except Subscription.DoesNotExist:
            subscription = Subscription()
            subscription.email = email

        subscription.subscribed = False
        subscription.location = location
        subscription.confirmation_requested_at = timezone.now()
        subscription.save()

        return Response()
