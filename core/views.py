# Built-in import
import json

# Django import
from django.http import HttpResponse,JsonResponse

# ORM import
from core.models import AssetData

def hola(request,asset):
    try:
        saved_asset = AssetData.objects.filter(asset__name__contains=asset)
        data = {
                "asset":asset,
                "values": [x.toJSON() for x in saved_asset]
            }
        return JsonResponse(data)
    except AssetData.DoesNotExist:
        return HttpResponse('Criptomoneda no figura en registros')
    