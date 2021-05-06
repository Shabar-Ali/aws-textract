import boto3
import os
from dotenv import load_dotenv

load_dotenv()

months = {
	"January": "1",
	"Feburary": "2",
	"March": "3",
	"April": "4",
	"May": "5",
	"June": "6",
	"July": "7",
	"August": "8",
	"September": "9",
	"October": "10",
	"November": "11",
	"December": "12"
}

def get_note_date():
	client = boto3.client('textract', region_name='ap-southeast-1',
	 	aws_access_key_id = os.getenv('aws_access_key_id'),
	    aws_secret_access_key = os.getenv('aws_secret_access_key'))

	response = client.start_document_text_detection(
	                DocumentLocation = {
	               		'S3Object': {
	               			'Bucket': 'textract-console-ap-southeast-1-e24fd2de-3562-46d5-b672-ccb9ed2', 
	               			'Name': 'Note.pdf'
	               		} 
	               	},
	               	ClientRequestToken="1111"
	            )
	jobId = response["JobId"]

	nextToken = None

	# Get the last paginated section on PDF
	while True:
		if nextToken == None:
			Response = client.get_document_text_detection(JobId=jobId)
		else:
			Response = client.get_document_text_detection(JobId=jobId, NextToken=nextToken)
		
		if "NextToken" in Response.keys():
			nextToken = Response["NextToken"]
		else:
			break

	# extract all text lines in the response
	blocks = Response['Blocks']
	all_lines = [l for l in blocks if l["BlockType"] == "LINE"]
	all_lines_text = [l["Text"] for l in all_lines]

	required_string = "Note on "

	# find the line which starts with "Note on " and extract the date
	for l in all_lines_text:
		s = l[0:8]
		if s == required_string:
			length = len(l)
			date = l[8:length-1]
			break


	# find and print the last hand writteb text
	# for l in all_lines_text:
	# 	if l[0:8] == "STATE OF":
	# 		state_of = l[0:11]
	# 	if l[0:9] == "COUNTY OF":
	# 		country_of = l[0:len(l)-1]

	# print(state_of)
	# print(country_of)

	day = ""
	month = ""
	year = ""
	temp = ""
	for x in date:
		if (x>='A' and x<='Z') or (x>='a' and x<='z') or (x>='0' and x<='9'):
			temp += x
		else:
			if month == "":
				month = months[temp]
			elif day == "":
				day = temp
			temp = ""
	year = temp

	date_on_note = month+'/'+day+'/'+year
	print()
	print("Commercial Promissory Note Date:", date_on_note)
	return date_on_note

get_note_date()






