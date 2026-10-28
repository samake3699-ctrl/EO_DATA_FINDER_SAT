
import json
from urllib.parse import urlencode, quote
from urllib.request import urlopen

BASE_URL = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"



def search_sikasso_october(
    start_date="2025-10-01",
    end_date="2025-11-01",
    max_cloud=10.0,
):

    filters = [
        "Collection/Name eq 'SENTINEL-2'",
        "contains(Name,'MSIL2A')",
        "OData.CSC.Intersects(area=geography'SRID=4326;POINT(-5.66654 11.31755)')",
        f"ContentDate/Start ge {start_date}T00:00:00.000Z",
        f"ContentDate/Start lt {end_date}T00:00:00.000Z",       
        f"Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' and att/OData.CSC.DoubleAttribute/Value le {max_cloud:.2f})",

    ]

    parameters = {
    "$filter": " and ".join(filters),
    "$top": 3,
    "$expand": "Attributes",
    }

    url = BASE_URL + "?" + urlencode(parameters, quote_via=quote)

    with urlopen(url, timeout=30) as response:
        return json.load(response)["value"]

def get_product_by_id(product_id):
    from uuid import UUID

    valid_id = str(UUID(product_id))

    url = f"{BASE_URL}({valid_id})?%24expand=Attributes"

    with urlopen(url, timeout=30) as response:
        return json.load(response)
