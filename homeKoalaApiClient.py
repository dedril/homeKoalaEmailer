import requests
from itertools import starmap, cycle

#dont change these values, they are set by homeKoala
ALPHA = 'abcdefghijklmnopqrstuvwxyz'
KEY = "hbt"

def getListings(lat,long,zip,bedrooms,maxPrice):
    type = "RENT"
    search_distance_in_meters = 2900
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
    print params

    response = requests.post("https://www.homekoala.com/ws/listing-search", data = params,headers=headers)

    return response.json()

def getListingDetail(sid):
    headers = {
                'Referer':'https://www.homekoala.com/map'
               }
    params = {
                "sid":sid
             }
    print params

    response = requests.post("https://www.homekoala.com/ws/rsl", data = params,headers=headers)

    #return the first one
    return response.json()[0]

def decrypt(message):#alg is vignere_decrypt

    def dec(c,k): return  "%s" % unichr(((ord(c) - ord(k)) % 256) )

    return "".join(starmap(dec, zip(message.decode('base64'), cycle(KEY))))
