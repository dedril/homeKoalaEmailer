# homeKoala Emailer

Simple script for crawling the homeKoala realestate website for new properties, and sending yourself an email.

## Installation
- Clone this repo into an ubuntu machine
- Ensure you have Python 2.7.6 and pip installed (http://www.saltycrane.com/blog/2010/02/how-install-pip-ubuntu/)
- Install the dependencies
  - sudo pip install requests
  - sudo pip install boto3
  - sudo pip install googlemaps
- setup your ~/.aws/credentials files to send emails via SES (http://docs.aws.amazon.com/aws-sdk-php/v2/guide/credentials.html#credential-profiles)
- get a google maps api key here https://console.developers.google.com/flows/enableapi?apiid=geocoding_backend&keyType=SERVER_SIDE&reusekey=true
- save your this key to an environment variable called GOOGLE_MAPS_API_KEY
- make sure 'Google Maps Geocoding API' is enabled for you here https://console.developers.google.com/apis/library?project=sacred-entry-119922
- run via 'python main.py' to start the script!

## Config
- the search config values can be found at the start of main.py
- the SES email config values can be found at the start of emailService.py
