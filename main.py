import re
import homeKoalaApiClient
import emailService
import googleMapsApiClient
import datetime
import requests.packages.urllib3
import urllib
requests.packages.urllib3.disable_warnings()
from cache import Cache

def main():

    #config goes here
    suburbs = ["Dee Why, sydney",
               "Cronulla, sydney",
               "Caringbah, sydney",
               "Miranda, sydney",
               "kirrawee, sydney",
                "Maroubra, sydney",
                "South Coogee, sydney",
                "Coogee, sydney",
                "Clovelly, sydney",
                "Bondi, sydney",
                "North Curl Curl, sydney",
                "Freshwater, sydney",
                "manly, sydney"
               ]

    #always exclude results that mention these words
    wordsToExclude = []

    numberOfBedRooms = "TWO"
    maxPricePerWeek = 700
    destinationEmailAddress = "homekoala@doddrell.com"
    search_distance_in_meters = 2900

    totalListings = []

    for suburb in suburbs:

        location = googleMapsApiClient.getLatLong(suburb)
        lat =location[0]
        long = location[1]

        listing_results = homeKoalaApiClient.getListings(lat, long, search_distance_in_meters, numberOfBedRooms, maxPricePerWeek)
        stats = homeKoalaApiClient.getStats(lat, long, search_distance_in_meters, numberOfBedRooms, maxPricePerWeek)

        cache = Cache()

        #also get any additional information we need.
        for x in listing_results["results"]:
            details = homeKoalaApiClient.getListingDetail(x["sourceId"])
            x["source_url"] =details["sourceUrl"]
            x["monthly_price"] = getMonthlyPrice(x["askingPrice"])

            x["min_price"] =getMonthlyPrice(stats["min"]["askingPrice"])
            x["median_price"] =getMonthlyPrice(stats["median"]["askingPrice"])
            x["max_price"] =getMonthlyPrice(stats["max"]["askingPrice"])

            if "frontCoverUrl" in x: #sometimes, no img....
                x["img_url"] = "https://www.homekoala.com/c/au?url=%s" % (urllib.quote_plus(x["frontCoverUrl"]))
            else:
                x["img_url"]= ''

            x["url_link"] = "https://www.homekoala.com/map/p/%s/?sb=r&c.d.pf=RENT&c.r.pz=%s,%s%%7C%s" % (x["sourceId"],lat,long,search_distance_in_meters)

            #print "%s, %s %s %s" % (x["pTitle"],x["min_price"],x["median_price"],x["max_price"])

            shouldInclude = True
            for word in wordsToExclude:
                shouldInclude = not (word.lower() in x["pTitle"].lower()) and \
                                not (word.lower() in details["description"].lower())
                if not shouldInclude:
                    print("excluding " + x["pTitle"] + " coz word found: " + word)
                    break

            if cache.haveSeenProperty(x["sourceId"]):
                shouldInclude = False

            if shouldInclude:
                totalListings.append(x)
                #mark as seen
                cache.markPropertyAsSeen(x["sourceId"])

    if len(totalListings) > 0:
        emailService.sendEmail(totalListings,destinationEmailAddress)
        print "%s: %s houses sent via email to %s" % (datetime.datetime.now(),len(totalListings), destinationEmailAddress)
    else:
        print "%s: No new updates today" % (datetime.datetime.now())

def getMonthlyPrice(price):
    return int(price) * 52 / 12

#helps us order the posts by a consistant value
def getUpdatedDateInDays(dateString):

    numbers = re.findall(r'\d+', dateString)
    number = 1 #if we cant see a number, assume the sentence is 'a month ago'
    if len(numbers) > 0:
        number = int(numbers[0])

    multilpier  = 1
    if "month" in dateString:
        multilpier = 30
    if "week" in dateString:
        multilpier = 7

    return number * multilpier

if __name__ == "__main__":
    main()
