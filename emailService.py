from email.mime.text import MIMEText

import boto3
import os
from email.mime.multipart import MIMEMultipart
import homeKoalaApiClient

#config
fromEmailAddress = 'homekoala@doddrell.com'


def sendEmail(listings,destination):

	msg = MIMEMultipart()
	msg['Subject'] = 'HomeKoala Listing Update'
	msg['From'] = fromEmailAddress
	msg['To'] = fromEmailAddress

	messageBody = """We're excited to bring you today's updated listings!"""

	for listing in listings:
		messageBody += getMessageForSingleListing(listing)

	part = MIMEText(messageBody,'html')
	msg.attach(part)

	#credentials are in ~/.aws/credentials
	#see more here http://docs.aws.amazon.com/aws-sdk-php/v2/guide/credentials.html#credential-profiles
	conn = boto3.client('ses', region_name='us-east-1')
	conn.send_raw_email(RawMessage= {'Data': msg.as_string()},Source=msg['From'],Destinations=[msg['To']])

def getMessageForSingleListing(listing):


	return """
			<hr/>
			<a href='%s'>
				$%s monthly - %s <br/>
				<img src='%s' width='300px'>
			</a>
			""" % (listing["source_url"], listing["monthly_price"], listing["pTitle"],listing["decrypted_img_url"])