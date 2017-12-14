from django.core.management.base import BaseCommand
from tempestatibus.api.models import Subscription, Location
from ._weather_service import WeatherService
from ._news_notifier import NewsNotifier


# Django Management Command to send newsletter
# to all the confirmed subscription
class Command(BaseCommand):

    help = 'Sends the newsletter to the subscribed receipts'
    weatherService = WeatherService()

    def handle(self, *args, **options):
        subscriptions = Subscription.objects.filter(
            subscribed=True).values()
        for subscription in subscriptions:
            try:
                self.processSubscription(subscription)
            except Exception as e:
                print(e)
                print('Unable to process Subscription ' +
                      str(subscription['id']))

    def processSubscription(self, subscription):
        subscription_id = subscription['id']
        subscription_email = subscription['email']
        subscription_location = Location.objects.get(
            id=subscription['location_id'])

        print(('Processing subscription id:{}' +
              ', email:{}, location:{}...').format(
                subscription_id,
                subscription_email, subscription_location.city_name))
        weatherData = Command.weatherService.classify(
            subscription_location.city_name)
        print("Subscription id:{} with {}".format(
            subscription_id, weatherData))

        newsNotifier = NewsNotifier(weatherData)
        newsNotifier.send_newsletter(
            subscription_email, subscription_location.city_name)

        print(('Completed processing subscription id:{}' +
              ', email:{}, location:{}.').format(
                subscription_id,
                subscription_email, subscription_location.city_name))
