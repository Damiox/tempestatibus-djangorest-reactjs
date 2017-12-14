import re
import json
import uuid
from datetime import timedelta
from django.conf import settings
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
    def post(self, request, *args, **kwarg):
        confirmation_id = kwarg.get('confirmation_id')
        try:
            subscription = Subscription.objects.get(
                confirmation_id=confirmation_id)
        except Subscription.DoesNotExist:
            raise exceptions.ParseError(
                detail="ConfirmationId is invalid")
        if self.is_confirmation_expired(subscription):
            raise exceptions.ParseError(
                detail="ConfirmationId is expired")

        isSubscribed = subscription.subscribed
        if isSubscribed is True:
            subscription.updated_at = timezone.now()
        else:
            subscription.subscribed = True
            subscription.subscribed_at = timezone.now()

        subscription.confirmation_id = None
        subscription.confirmation_requested_at = None
        subscription.save()
        return Response(status=200 if isSubscribed is True else 201)

    def is_confirmation_expired(self, subscription):
        now = timezone.now()
        requested_at = subscription.confirmation_requested_at
        return now - requested_at > timedelta(hours=24)


class ConfirmUnsubscriptionView(generics.GenericAPIView):
    '''
        API to confirm an unsubscription. After an unsubscription is confirmed,
        it won't receive any more newsletters until next re-subscription.
    '''
    def post(self, request, *args, **kwarg):
        confirmation_id = kwarg.get('confirmation_id')
        try:
            subscription = Subscription.objects.get(
                confirmation_id=confirmation_id)
        except Subscription.DoesNotExist:
            raise exceptions.ParseError(
                detail="ConfirmationId is invalid")
        if subscription.subscribed is not True:
            raise exceptions.ParseError(
                detail="User is already unsubscribed")

        subscription.subscribed = False
        subscription.unsubscribed_at = timezone.now()
        subscription.confirmation_id = None
        subscription.confirmation_requested_at = None
        subscription.save()
        return Response()


class SubscribeReceiptView(generics.GenericAPIView):
    '''
        API to request a subscription. A subscription needs to be confirmed
        by the User. If the User exists, then it means the User may be trying
        to update their info.
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
        except Subscription.DoesNotExist:
            subscription = Subscription()
            subscription.email = email
            subscription.subscribed = False

        subscription.location = location
        subscription.confirmation_id = uuid.uuid4()
        subscription.confirmation_requested_at = timezone.now()
        subscription.save()

        # we should wrap this into a transaction, and save the
        # subscription iff the email has been sent successfully
        confirmation_url = '{}/confirm-subscription/{}'.format(
                settings.API_URL, str(subscription.confirmation_id))
        if subscription.subscribed is False:
            confirmation_subject = 'Please confirm your subscription'
            confirmation_msg_plain = ('You need to confirm your ' +
                                      'subscription. ' +
                                      'Email:{} ; Location:{} - ' +
                                      'Please open your browser and ' +
                                      'go to {}.').format(
                    email, location.city_name, confirmation_url)
            confirmation_msg_html = ('You need to confirm your ' +
                                     'subscription. ' +
                                     'Email:{} ; Location:{} - ' +
                                     'Please click <a href="{}">' +
                                     'here</a>.').format(
                    email, location.city_name, confirmation_url)
        else:
            confirmation_subject = 'Please confirm the update on your ' +\
                'subscription'
            confirmation_msg_plain = ('You need to confirm the update on ' +
                                      'your subscription. ' +
                                      'Email:{} ; Location:{} - ' +
                                      'Please open your browser and ' +
                                      'go to {}.').format(
                    email, location.city_name, confirmation_url)
            confirmation_msg_html = ('You need to confirm the update on ' +
                                     'your subscription. ' +
                                     'Email:{} ; Location:{} - ' +
                                     'Please click <a href="{}">' +
                                     'here</a>.').format(
                    email, location.city_name, confirmation_url)

        emailService = EmailService()
        emailService.send(
            subscription.email,
            confirmation_subject,
            confirmation_msg_plain, confirmation_msg_html, None)

        return Response()


class UnsubscribeReceiptView(generics.GenericAPIView):
    '''
        API to request an unsubscription. An unsubscription needs to be
        confirmed by the User.
    '''
    def post(self, request, *args, **kwarg):
        # Parsing request body
        body = json.loads(request.body.decode('utf-8'))

        # Validating body
        if 'email' not in body:
            raise exceptions.ParseError(
                detail="email is missing")

        email = body['email']
        # Completed validating body

        try:
            subscription = Subscription.objects.get(email=email)
            if subscription.subscribed is False:
                raise exceptions.ParseError(
                    detail="Email is already unsubscribed")
        except Subscription.DoesNotExist:
            raise exceptions.ParseError(
                    detail="Email cannot be found")

        subscription.confirmation_id = uuid.uuid4()
        subscription.confirmation_requested_at = timezone.now()
        subscription.save()

        # we should wrap this into a transaction, and save the
        # subscription iff the email has been sent successfully
        confirmation_url = '{}/confirm-unsubscription/{}'.format(
            settings.API_URL, str(subscription.confirmation_id))
        confirmation_msg_plain = 'You need to confirm your unsubscription. ' +\
            'Please open your browser and go to {}.'.format(confirmation_url)
        confirmation_msg_html = 'You need to confirm your unsubscription. ' +\
            'Please click <a href="{}">here</a>.'.format(confirmation_url)

        emailService = EmailService()
        emailService.send(
            subscription.email,
            'You requested to be unsubscribed. You need to confirm ' +
            'this action.',
            confirmation_msg_plain, confirmation_msg_html, None)

        return Response()
