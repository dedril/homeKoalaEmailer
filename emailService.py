# coding: utf-8
from email.mime.text import MIMEText
from sys import argv
import boto3
import os
from email.mime.multipart import MIMEMultipart
import homeKoalaApiClient
import codecs

#config
fromEmailAddress = 'homekoala@doddrell.com'


def sendEmail(listings,destination):

	msg = MIMEMultipart()
	msg['Subject'] = 'HomeKoala Listing Update'
	msg['From'] = fromEmailAddress
	msg['To'] = fromEmailAddress

	messageBody = """"""

	leftTemplate = codecs.open('./emailTemplateLeft.html', encoding='utf-8').read().encode('ascii', 'ignore')
	rightTemplate = codecs.open('./emailTemplateRight.html', encoding='utf-8').read().encode('ascii', 'ignore')

	isRightSide = True
	for listing in listings:
		if isRightSide:
			messageBody += populateTemplate(rightTemplate,listing)
		else:
			messageBody += populateTemplate(leftTemplate,listing)

		isRightSide = not isRightSide

	test = codecs.open('./emailTemplate.html', encoding='utf-8').read().encode('ascii', 'ignore').replace('REPLACE_ME',messageBody)

	part = MIMEText(test,'html')
	msg.attach(part)

	#credentials are in ~/.aws/credentials
	#see more here http://docs.aws.amazon.com/aws-sdk-php/v2/guide/credentials.html#credential-profiles
	conn = boto3.client('ses', region_name='us-east-1')
	conn.send_raw_email(RawMessage= {'Data': msg.as_string()},Source=msg['From'],Destinations=[msg['To']])

def populateTemplate(template,listing):

	amountWithCommas = "{:,}".format(listing["monthly_price"])
	monthlyPriceText = "${0} per month".format(amountWithCommas)

	populatedTemplate = template.replace('IMAGE_SRC',listing["img_url"])
	populatedTemplate = populatedTemplate.replace('DETAILS_TEXT',monthlyPriceText)
	populatedTemplate = populatedTemplate.replace('HEADER',listing["pTitle"])
	populatedTemplate = populatedTemplate.replace('LINK',listing["source_url"])

	return populatedTemplate

