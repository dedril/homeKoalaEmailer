import os
import googlemaps
import json

def getLatLong(address):
    #see more at https://github.com/googlemaps/google-maps-services-python
    #and https://developers.google.com/maps/documentation/geocoding/intro
    key = os.environ.get('GOOGLE_MAPS_API_KEY')

    gmaps = googlemaps.Client(key=key)
    result  = gmaps.geocode(address)

    #print json.dumps(result,sort_keys=True,indent=4, separators=(',', ': '))

    lat =result[0]["geometry"]["location"]["lat"]
    lng = result[0]["geometry"]["location"]["lng"]

    return lat,lng

def getZip(lat,long):
    key = os.environ.get('GOOGLE_MAPS_API_KEY')

    gmaps = googlemaps.Client(key=key)
    result = gmaps.reverse_geocode((lat,long))
    #print json.dumps(result,sort_keys=True,indent=4, separators=(',', ': '))

    address_components = result[0]["address_components"]
    zip =  address_components[len(address_components) -1]["long_name"]

    return zip


if __name__ == "__main__":
    print getLatLong("gladesville, sydney")
    print getZip(-33.8324481, 151.1270573)