import re
import homeKoalaApiClient
import emailService
import googleMapsApiClient


def main():

    #config goes here
    suburbs = ["Gladesville, sydney",
               "AUBURN, sydney",
               "Marrickville, sydney",
               "Ryde, sydney",
               "West Ryde, sydney"]

    numberOfBedRooms = "TWO"
    maxPricePerWeek = 700
    destinationEmailAddress = "homekoala@doddrell.com"
    totalListings = []

    for suburb in suburbs:

        location = googleMapsApiClient.getLatLong(suburb)
        lat =location[0]
        long = location[1]
        zipcode = googleMapsApiClient.getZip(lat,long)

        json_results = homeKoalaApiClient.getListings(lat, long, zipcode, numberOfBedRooms, maxPricePerWeek)

        #also get any additional information we need.
        for x in json_results["results"]:
            details = homeKoalaApiClient.getListingDetail(x["sourceId"])
            x["source_url"] =details["sourceUrl"]
            x["monthly_price"] = int(x["askingPrice"]) * 52 / 12

            if "frontCoverUrl" in x: #sometimes, no img....
                x["decrypted_img_url"] = homeKoalaApiClient.decrypt(x["frontCoverUrl"])
            else:
                x["decrypted_img_url"]= ''

            totalListings.append(x)

    #always have the most recent first.
    totalListings = sorted(totalListings, key= lambda x: getUpdatedDateInDays(x["listingDate"]) , reverse=False )

    emailService.sendEmail(totalListings,destinationEmailAddress)

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
