from urllib.request import urlopen
from json import load

from concurrent.futures import ThreadPoolExecutor, as_completed
def show_routes_print(enderecos):
    routers = []

    for endereco in enderecos:
        router = address_info(endereco)
        routers.append(router)

    print(f"Rota percorrida:\n{' -> '.join(routers)}")

def address_info(address): 
    data = ipInfo(address)
    if data:
        return info_validation(data)
    else:
        return "_"

def info_validation(data):
    city = data.get("city", "")
    region = data.get("region", "")
    country = data.get("country", "")
    org = data.get("org", "")

    return format_data(city, region, country, org)

def format_data(city, region, country, org):
    if not city and not region and not country and not org:
        return "_"

    city = city if city else "???"
    region = region if region else "???"
    country = country if country else "???"
    org = org if org else "???"

    return f"{org}\n{city}, {region} - {country}"

def ipInfo(address):
    if address == '' or address == '*':
        return None

    url = f'https://ipinfo.io/{address}/json'
    try:
        with urlopen(url) as response:
            data = load(response)
            return data
    except Exception as e:
        print(f"Error fetching data for {address}: {e}")
        return None

