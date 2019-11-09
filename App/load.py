import os
from django.contrib.gis.utils import LayerMapping
from .models import County, ElectoralDivision, SmallArea


data = [
    {
        "data_file": "Census2011_Counties_Modified",
        "data_class": County,
        "mapping": {
            'nuts1': 'NUTS1',
            'nuts1name': 'NUTS1NAME',
            'nuts2': 'NUTS2',
            'nuts2name': 'NUTS2NAME',
            'nuts3': 'NUTS3',
            'nuts3name': 'NUTS3NAME',
            'county': 'COUNTY',
            'countyname': 'COUNTYNAME',
            'male2011': 'Male2011',
            'female2011': 'Female2011',
            'total2011': 'Total2011',
            'ppocc2011': 'PPOcc2011',
            'unocc2011': 'Unocc2011',
            'hs2011': 'HS2011',
            'vacant2011': 'Vacant2011',
            'pcvac2011': 'PCVac20111',
            'total_area': 'TOTAL_AREA',
            'land_area': 'LAND_AREA',
            'createdate': 'CREATEDATE',
            'geogid': 'GEOGID',
            'geom': 'MULTIPOLYGON',
        },
    },
    {
        "data_file": "Census2011_Electoral_Divisions_Modified",
        "data_class": ElectoralDivision,
        "mapping": {
            'nuts1': 'NUTS1',
            'nuts1name': 'NUTS1NAME',
            'nuts2': 'NUTS2',
            'nuts2name': 'NUTS2NAME',
            'nuts3': 'NUTS3',
            'nuts3name': 'NUTS3NAME',
            'county': 'COUNTY',
            'countyname': 'COUNTYNAME',
            'csoed': 'CSOED',
            'osied': 'OSIED',
            'edname': 'EDNAME',
            'male2011': 'Male2011',
            'female2011': 'Female2011',
            'total2011': 'Total2011',
            'ppocc2011': 'PPOcc2011',
            'unocc2011': 'Unocc2011',
            'hs2011': 'HS2011',
            'vacant2011': 'Vacant2011',
            'pcvac2011': 'PCVac2011',
            'total_area': 'TOTAL_AREA',
            'land_area': 'LAND_AREA',
            'createdate': 'CREATEDATE',
            'geogid': 'GEOGID',
            'highered': 'HigherEd',
            'geom': 'MULTIPOLYGON',
        },
    },
    {
        "data_file": "Census2011_Small_Areas_Modified",
        "data_class": SmallArea,
        "mapping": {
            'nuts1': 'NUTS1',
            'nuts1name': 'NUTS1NAME',
            'nuts2': 'NUTS2',
            'nuts2name': 'NUTS2NAME',
            'nuts3': 'NUTS3',
            'nuts3name': 'NUTS3NAME',
            'county': 'COUNTY',
            'countyname': 'COUNTYNAME',
            'csoed': 'CSOED',
            'osied': 'OSIED',
            'edname': 'EDNAME',
            'small_area': 'SMALL_AREA',
            'male2011': 'Male2011',
            'female2011': 'Female2011',
            'total2011': 'Total2011',
            'ppocc2011': 'PPOcc2011',
            'unocc2011': 'Unocc2011',
            'hs2011': 'HS2011',
            'vacant2011': 'Vacant2011',
            'pcvac2011': 'PCVac2011',
            'createdate': 'CREATEDATE',
            'geogid': 'GEOGID',
            'geom': 'MULTIPOLYGON',
        }
    }
]


def run(verbose=True):
    for entry in data:
        file_name = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data', f'{entry["data_file"]}.shp'),
        )

        old_data = entry["data_class"].objects.all()
        for item in old_data:
            item.delete()

        print("-"*80)
        print(f"{file_name}\n{entry['data_class']}\n{entry['mapping']}")
        lm = LayerMapping(entry["data_class"], file_name, entry["mapping"], transform=False)
        lm.save(strict=True, verbose=verbose)
