import re
import json
from datetime import timedelta
from django.utils import timezone
from rest_framework import generics, exceptions
from rest_framework.response import Response
from tempestatibus.api.models import Subscription, Location
from tempestatibus.api.serializers import LocationSerializer
from tempestatibus.api.management.commands._email_service import EmailService


class LocationView(generics.GenericAPIView):
    '''
        API to get all the locations
    '''
    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)


class ConfirmSubscriptionView(generics.GenericAPIView):
    '''
        API to confirm a subscription. After a subscription is confirmed,
        it is ready to start receiving newsletters
    '''
    def get(self, request, *args, **kwarg):
        confirmation_id = kwarg.get('confirmation_id')
        try:
            subscription = Subscription.objects.get(
                confirmation_id=confirmation_id)
        except Subscription.DoesNotExist:
            raise exceptions.ParseError(
                detail="ConfirmationId is invalid")
        if subscription.subscribed is True:
            raise exceptions.ParseError(
                detail="Subscription was already confirmed")
        if self.is_confirmation_expired(subscription):
            raise exceptions.ParseError(
                detail="ConfirmationId is expired")

        subscription.subscribed = True
        subscription.subscribed_at = timezone.now()
        subscription.save()
        return Response()

    def is_confirmation_expired(self, subscription):
        now = timezone.now()
        requested_at = subscription.confirmation_requested_at
        return now - requested_at > timedelta(hours=24)


class SubscribeReceiptView(generics.GenericAPIView):
    '''
        API to request a subscription. A subscription needs to be confirmed
        by the User.
    '''
    def post(self, request, *args, **kwarg):
        # Parsing request body
        body = json.loads(request.body.decode('utf-8'))

        # Validating body
        if 'email' not in body:
            raise exceptions.ParseError(
                detail="email is missing")
        if 'city_name' not in body:
            raise exceptions.ParseError(
                detail="city_name is missing")

        email = body['email']
        city_name = body['city_name']

        if not re.compile(r"[^@]+@[^@]+\.[^@]+").match(email):
            raise exceptions.ParseError(
                detail="email is invalid")

        try:
            location = Location.objects.get(city_name=city_name)
        except Location.DoesNotExist:
            raise exceptions.ParseError(
                detail="City Invalid")
        # Completed validating body

        try:
            subscription = Subscription.objects.get(email=email)
            if subscription.subscribed is True:
                raise exceptions.ParseError(
                    detail="Email is already subscribed")
        except Subscription.DoesNotExist:
            subscription = Subscription()
            subscription.email = email

        subscription.subscribed = False
        subscription.location = location
        subscription.confirmation_requested_at = timezone.now()
        subscription.save()

        # we should wrap this into a transaction, and save the
        # subscription iff the email has been sent successfully
        confirmation_url = request.build_absolute_uri('/')[:-1]
        + '/confirm-subscription/' + str(subscription.confirmation_id)
        confirmation_msg_plain = 'You need to confirm your subscription. '
        'Please open your browser and go to {}.'.format(confirmation_url)
        confirmation_msg_html = 'You need to confirm your subscription. '
        'Please click <a href="{}">here</a>.'.format(confirmation_url)

        emailService = EmailService()
        emailService.send(
            subscription.email,
            'Please confirm your subscription',
            confirmation_msg_plain, confirmation_msg_html, None)

        return Response()
