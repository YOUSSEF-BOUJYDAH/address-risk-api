from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'label', 'housenumber', 'street', 'postcode', 'citycode', 'latitude', 'longitude']