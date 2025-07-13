from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Try to get data from cache
    properties = cache.get('all_properties')

    if properties is None:
        # If not in cache, fetch from DB
        properties = list(Property.objects.all().values())
        # Cache it for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)

    return properties
