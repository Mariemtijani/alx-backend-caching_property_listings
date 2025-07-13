from django.shortcuts import render
from django.http import JsonResponse
from .models import Property
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # cache for 15 minutes
def property_list(request):
    properties = Property.objects.all().values()
    return JsonResponse(list(properties), safe=False)
