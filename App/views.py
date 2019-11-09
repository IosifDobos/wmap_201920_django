from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse_lazy
from . import models
from django.contrib.gis.geos import Point, Polygon
from django.http import JsonResponse
from django.core.serializers import serialize
import json


class BaseLayout(TemplateView):
    template_name = 'base.html'

class MapPage(LoginRequiredMixin, TemplateView):
    template_name = 'App/map_page.html'
    login_url = reverse_lazy("app:login")


class About(LoginRequiredMixin, TemplateView):
    template_name = 'App/about.html'
    login_url = reverse_lazy("app:login")


@login_required(login_url=reverse_lazy("app:login"))
def get_ED_my_location(request):
    try:
        point = request.GET["point"].split(",")
        point = [float(part) for part in point]
        point = Point(point, srid=4326)
        ed_set = serialize("geojson", models.ElectoralDivision.objects.filter(
            geom__intersects=point
        ))

        return JsonResponse(json.loads(ed_set), status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)


@login_required(login_url=reverse_lazy("app:login"))
def get_ED_bbox(request):
    try:
        bbox = request.GET["bbox"].split(",")
        bbox = [float(part) for part in bbox]
        bbox = Polygon.from_bbox(bbox)
        bbox.srid = 4326
        ed_set = serialize("geojson", models.ElectoralDivision.objects.filter(
            geom__intersects=bbox
        ))

        return JsonResponse(json.loads(ed_set), status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)


@login_required(login_url=reverse_lazy("app:login"))
def update_position_db(request):
    try:
        user_profle = models.UserProfile.objects.get(owner=request.user)
        if not user_profle:
            raise ValueError("Can't get User details")

        point = request.POST["point"].split(",")
        point = [float(part) for part in point]
        point = Point(point, srid=4326)

        user_profle.last_location = point
        user_profle.save()

        return JsonResponse({"message": f"Set location to {point.wkt}."}, status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)
