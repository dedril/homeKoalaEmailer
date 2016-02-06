import requests
import requests.packages.urllib3
import urllib
requests.packages.urllib3.disable_warnings()
import googleMapsApiClient


def getListings(lat,long,search_distance_in_meters,bedrooms,maxPrice):
    type = "RENT"

    location_param = "%s,%s|%s" % (lat,long,search_distance_in_meters)
    price_param  ="*-%s" % (maxPrice)
    headers = {
                'Referer':'https://www.homekoala.com/map'
               }
    params = {
                "c.r.pz":location_param,
                "c.d.pf":type,
                "c.d.br":bedrooms,
                "f.pr":price_param,
                "mini":False
             }
    #print params

    response = requests.post("https://www.homekoala.com/ws/listing-search", data = params,headers=headers)

    return response.json()

def getStats(lat,long,search_distance_in_meters,bedrooms,maxPrice):

    type = "RENT"
    location_param = "%s,%s|%s" % (lat,long,search_distance_in_meters)
    price_param  ="*-%s" % (maxPrice)
    headers = {
                'Referer':'https://www.homekoala.com/map'
               }

    params = {
                "c.r.pz":location_param,
                "c.d.pf":type,
                "c.d.br":bedrooms,
                "f.pr":price_param,
                "mini":False
             }

    #print params

    response = requests.post("https://www.homekoala.com/ws/geo-search", data = params,headers=headers)

    json = response.json()

    #print json["stats"]["prices"]

    return json["stats"]["prices"]

def getListingDetail(sid):
    headers = {
                'Referer':'https://www.homekoala.com/map'
               }
    params = {
                "sid":sid
             }
    #print params

    response = requests.post("https://www.homekoala.com/ws/rsl", data = params,headers=headers)

    #return the first one
    return response.json()[0]

if __name__ == "__main__":
    suburb = "Gladesville, sydney"

    numberOfBedRooms = "TWO"
    maxPricePerWeek = 700
    search_distance_in_meters = 2900

    location = googleMapsApiClient.getLatLong(suburb)
    lat =location[0]
    long = location[1]

    #listing_results = homeKoalaApiClient.getListings(lat, long, search_distance_in_meters, numberOfBedRooms, maxPricePerWeek)
    stats = getStats(lat, long, search_distance_in_meters, numberOfBedRooms, maxPricePerWeek)

    print "%s %s %s" % (stats["min"]["askingPrice"],stats["median"]["askingPrice"],stats["max"]["askingPrice"])


