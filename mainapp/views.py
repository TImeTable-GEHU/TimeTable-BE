import json

from Constants.is_conflict import IsConflict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from mainapp.converter.converter import csv_to_json

