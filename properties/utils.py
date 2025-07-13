import logging
from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_all_properties():
    # Try to get data from cache
    properties = cache.get('all_properties')

    if properties is None:
        # If not in cache, fetch from DB
        properties = list(Property.objects.all().values())
        # Cache it for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)

    return properties

def get_redis_cache_metrics():
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses
        hit_ratio = hits / total_requests if total_requests > 0 else 0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": hit_ratio
        }

        logger.error("Redis Cache Metrics: %s", metrics)
        return metrics

    except Exception as e:
        logger.error("Failed to get Redis metrics: %s", str(e))
        return {"hits": 0, "misses": 0, "hit_ratio": 0}