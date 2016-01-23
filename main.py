import re
import homeKoalaApiClient
import emailService
import googleMapsApiClient


def main():

    #config goes here
    suburb = "gladsville, sydney"
    numberOfBedRooms = "TWO"
    maxPricePerWeek = 700
    destinationEmailAddress = "homekoala@doddrell.com"

    location = googleMapsApiClient.getLatLong(suburb)
    lat =location[0]
    long = location[1]
    zipcode = googleMapsApiClient.getZip(lat,long)

    json_results = homeKoalaApiClient.getListings(lat, long, zipcode, numberOfBedRooms, maxPricePerWeek)

    #always have the most recent first.
    listings = sorted(json_results["results"], key= lambda x: getUpdatedDateInDays(x["listingDate"]) , reverse=False )

    #also get any additional information we need.
    for x in listings:
        details = homeKoalaApiClient.getListingDetail(x["sourceId"])
        x["source_url"] =details["sourceUrl"]
        x["monthly_price"] = int(x["askingPrice"]) * 52 / 12

        if "frontCoverUrl" in x: #sometimes, no img....
            x["decrypted_img_url"] = homeKoalaApiClient.decrypt(x["frontCoverUrl"])
        else:
            x["decrypted_img_url"]= ''


    emailService.sendEmail(listings,destinationEmailAddress)

    print "email sent"

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
