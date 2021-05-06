from promissory_note import get_note_date 
from credit_report import get_credit_report_details
from datetime import datetime

credit_date, credit_score = get_credit_report_details()
note_date = get_note_date()

date_format = "%m/%d/%Y"

a = datetime.strptime(credit_date, date_format)
b = datetime.strptime(note_date, date_format)
delta = b - a
print()
print("Credit Report is",delta.days,"days old") 
print()
print("Credit Score:", credit_score)
