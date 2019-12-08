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
from django.utils import timezone
import requests


class BaseLayout(TemplateView):
    template_name = 'base.html'

class MapPage(LoginRequiredMixin, TemplateView):
    template_name = 'App/map_page.html'
    login_url = reverse_lazy("app:login")


class About(LoginRequiredMixin, TemplateView):
    template_name = 'App/about.html'
    login_url = reverse_lazy("app:login")


class Compass(LoginRequiredMixin, TemplateView):
    template_name = 'App/compass.html'
    login_url = reverse_lazy("app:login")


class Directions(LoginRequiredMixin, TemplateView):
    template_name = 'App/directions_page.html'
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


@login_required(login_url=reverse_lazy("app:login"))
def get_amenities(request):
    """
    make a call to Overpass API and return the results of a search in GeoJSON

    :param request: Incoming request includes a search string and a bbox string
    :return: Results in GeoJSON
    """
    import overpy
    api = overpy.Overpass()

    amenity = bbox = ""
    if "amenity" in request.GET:
        amenity = request.GET["amenity"]
    if amenity:
        amenity = amenity.lower()
    if "bbox" in request.GET:
        bbox = request.GET["bbox"]


    query = """
    [out:json][timeout:25]; 
    (
        node({1})["amenity"="{0}"]; 
        way({1})["amenity"="{0}"]; 
        rel({1})["amenity"="{0}"]; 
    ); 
    out center body qt; 
    """.format(amenity, bbox)

    try:
        result = api.query(query)

        result_geojson = {"type": "FeatureCollection", "features": []}

        for node in result.nodes:
            this_feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [None, None]
                },
                "properties": {
                }
            }

            this_feature["geometry"]["coordinates"][0] = float(node.lon)
            this_feature["geometry"]["coordinates"][1] = float(node.lat)

            for tag in node.tags:
                this_feature["properties"][tag] = node.tags[tag]

            result_geojson["features"].append(this_feature)

        for way in result.ways:
            this_feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [None, None]
                },
                "properties": {
                }
            }

            this_feature["geometry"]["coordinates"][0] = float(way.center_lon)
            this_feature["geometry"]["coordinates"][1] = float(way.center_lat)

            for tag in way.tags:
                this_feature["properties"][tag] = way.tags[tag]

            result_geojson["features"].append(this_feature)

        return JsonResponse(result_geojson, status=200)

    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)


def get_magnetic_declination(request):
    try:
        location = json.loads(request.GET["my_location"])
        lat = f"{location['lat']}"
        lon = f"{location['lon']}"
        now = timezone.now().isoformat().split("T")[0]
        URL = f"http://geomag.bgs.ac.uk/web_service/GMModels/wmm/2015v2/?" \
              f"latitude={lat}&longitude={lon}&altitude=0&date={now}&format=json"

        response = requests.get(URL)
        if response.status_code > 399:
            raise ValueError(f"HTTP status code is {response.status_code} - {response.reason}. ")

        return JsonResponse(response.json(), status=200)
    except Exception as e:
        return JsonResponse({"message": f"{e}"}, status=400)