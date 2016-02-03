import re
import homeKoalaApiClient
import emailService
import googleMapsApiClient
import datetime
import requests.packages.urllib3
import urllib
requests.packages.urllib3.disable_warnings()

def main():

    #config goes here
    suburbs = ["Gladesville, sydney",
               "AUBURN, sydney",
               "Marrickville, sydney",
               "Ryde, sydney",
               "darlinghurst, sydney",
               "West Ryde, sydney"]

    #always exclude results that mention these words
    wordsToExclude = ["unit",
                      "apartment"]

    numberOfBedRooms = "TWO"
    maxPricePerWeek = 700
    destinationEmailAddress = "homekoala@doddrell.com"
    search_distance_in_meters = 2900

    totalListings = []

    for suburb in suburbs:

        location = googleMapsApiClient.getLatLong(suburb)
        lat =location[0]
        long = location[1]

        json_results = homeKoalaApiClient.getListings(lat, long, search_distance_in_meters, numberOfBedRooms, maxPricePerWeek)

        #also get any additional information we need.
        for x in json_results["results"]:
            details = homeKoalaApiClient.getListingDetail(x["sourceId"])
            x["source_url"] =details["sourceUrl"]
            x["monthly_price"] = int(x["askingPrice"]) * 52 / 12

            if "frontCoverUrl" in x: #sometimes, no img....
                x["img_url"] = "https://www.homekoala.com/c/au?url=%s" % (urllib.quote_plus(x["frontCoverUrl"]))
            else:
                x["img_url"]= ''

            x["url_link"] = "https://www.homekoala.com/map/p/%s/?sb=r&c.d.pf=RENT&c.r.pz=%s,%s%%7C%s" % (x["sourceId"],lat,long,search_distance_in_meters)

            shouldInclude = True
            for word in wordsToExclude:
                shouldInclude = not (word.lower() in x["pTitle"].lower()) and \
                                not (word.lower() in details["description"].lower())
                if not shouldInclude:
                    print("excluding " + x["pTitle"] + " coz word found: " + word)
                    break

            if shouldInclude:
                totalListings.append(x)

    #always have the most recent first.
    totalListings = sorted(totalListings, key= lambda x: getUpdatedDateInDays(x["listingDate"]) , reverse=False )


    emailService.sendEmail(totalListings,destinationEmailAddress)

    print "%s: %s houses sent via email to %s" % (datetime.datetime.now(),len(totalListings), destinationEmailAddress)

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
