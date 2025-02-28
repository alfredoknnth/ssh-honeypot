import geoip2.database
from config import GEOIP_DB_PATH

def get_location(ip):
    with geoip2.database.Reader(GEOIP_DB_PATH) as reader:
        match = reader.city(ip)
        if match: 
            city = match.city.name
            country = match.country.name
    return (city, country)