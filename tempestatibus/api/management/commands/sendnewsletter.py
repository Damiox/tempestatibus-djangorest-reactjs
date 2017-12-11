

from django.core.management.base import BaseCommand, CommandError
from tempestatibus.api.models import Subscription, Location
from ._weather_service import WeatherService

class Command(BaseCommand):
	
	help = 'Sends the newsletter to the subscribed receipts'
	weatherService = WeatherService()

	def handle(self, *args, **options):
		subscriptions = Subscription.objects.filter(subscribed=True).values()
		for subscription in subscriptions:
			self.processSubscription(subscription)

	def processSubscription(self, subscription):
		subscription_id = subscription['id']
		subscription_email = subscription['email']
		subscription_location = Location.objects.get(id=subscription['location_id']); 

		print("Processing Subscription id:{}, email:{}, location:{}...".format(
			subscription_id, subscription_email, subscription_location.city_name)
		)
		weatherData = Command.weatherService.classify(subscription_location.city_name)
		print(weatherData.get_weather())
		print(weatherData.get_temp_curr())
		print(weatherData.get_temp_diff_avg())

