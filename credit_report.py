# NOTE: get_document_text_detection returns paginated response with 1000 blocks in each response, so first response contains approx 2 pages of pdf 

import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def get_credit_report_date(all_lines_text):
	required_string = "Date: "
	# match if the line start with "Date: " and extract the date
	for l in all_lines_text:
		s = l[0:6]
		if s == required_string:
			length = len(l)
			date = l[6:length]
			break
	print()
	print("Credit Report Date: ", date)
	return date


def get_credit_scores(all_lines_text):
	credit_scores = []
	found = False

	for l in all_lines_text:
		if found:
			credit_scores.append(int(l))
			if len(credit_scores) == 3:
				break
		if l == "Bureau Scores":
			found = True

	credit_scores.sort()
	print()
	print("All Credit Scores: ",credit_scores)
	return credit_scores[1]



def get_credit_report_details():
	client = boto3.client('textract', region_name='ap-southeast-1',
	 	aws_access_key_id = os.getenv('aws_access_key_id'),
	    aws_secret_access_key = os.getenv('aws_secret_access_key'))

	response = client.start_document_text_detection(
	                DocumentLocation = {
	               		'S3Object': {
	               			'Bucket': 'textract-console-ap-southeast-1-e24fd2de-3562-46d5-b672-ccb9ed2', 
	               			'Name': 'jose_deleon___credit_report.pdf'
	               		} 
	               	},
	               	ClientRequestToken="1111222"
	            )

	jobId = response["JobId"]
	response = client.get_document_text_detection(JobId=jobId)

	blocks = response['Blocks']
	all_lines = [l for l in blocks if l["BlockType"] == "LINE"]
	all_lines_text = [l["Text"] for l in all_lines]

	report_date = get_credit_report_date(all_lines_text)
	credit_score = get_credit_scores(all_lines_text)

	return report_date, credit_score
