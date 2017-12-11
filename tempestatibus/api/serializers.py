from rest_framework import serializers
from tempestatibus.api.models import Location

class LocationSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Location
		fields = ('city_name', )
