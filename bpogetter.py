import imaplib
import email
import datetime
import re

# Your email credentials
EMAIL = 'careersglobal@unitedinvestmentsfirm.com'
EMAIL = 'bpo@unitedinvestmentsfirm.com'
# EMAIL = 'bpos@unitedinvestmentsfirm.com'
PASSWORD = 'Bpos2020'
IMAP_SERVER = 'mail.unitedinvestmentsfirm.com'

# Print your personal email and host
print(f"Customer Email: {EMAIL}")
host = IMAP_SERVER.split("mail.")[-1]
print(f"Host: {host}\n")

# Connect to your mailbox using IMAP
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)
mail.select('inbox')

# Search for emails from the past 3 days
three_days_ago = (datetime.datetime.now() - datetime.timedelta(days=90)).strftime('%d-%b-%Y')
status, email_ids = mail.search(None, '(SINCE "' + three_days_ago + '")')

# Keywords to search for in the email subject
subject_keywords = ["bid", "request", "assignment"]

# Patterns to extract information from the email body
fee_pattern = re.compile(r'fee:\s*\$?(\d+(\.\d{2})?)', re.IGNORECASE)
city_pattern = re.compile(r'city:\s*(\w+)', re.IGNORECASE)
due_date_pattern = re.compile(r'order due date:\s*(\w+ \d+, \d+)', re.IGNORECASE)
product_pattern = re.compile(r'product:\s*(\w+)', re.IGNORECASE)

# Counter for emails that match the criteria
counter = 0

# Iterate through all emails
for e_id in email_ids[0].split():
    status, email_data = mail.fetch(e_id, '(RFC822)')
    raw_email = email_data[0][1]

    # Parse the raw email
    msg = email.message_from_bytes(raw_email)
    email_subject = msg['subject']
    email_from = msg['from']
    email_date = msg['date']
    # email_body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if "attachment" not in content_disposition and content_type == "text/plain":
                email_body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                break
    else:
        email_body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')


    # Check if the email subject contains the keywords
    if email_subject and any(keyword.lower() in email_subject.lower() for keyword in subject_keywords):
        fee_match = fee_pattern.search(email_body)
        city_match = city_pattern.search(email_body)
        due_date_match = due_date_pattern.search(email_body)
        product_match = product_pattern.search(email_body)

        fee = fee_match.group(1) if fee_match else 'N/A'
        city = city_match.group(1) if city_match else 'N/A'
        due_date = due_date_match.group(1) if due_date_match else 'N/A'
        product = product_match.group(1) if product_match else 'N/A'

        counter += 1
        print(f"Email {counter}:")
        print(f"From: {email_from}")
        print(f"Fee: ${fee}")
        print(f"City: {city}")
        print(f"Order Due Date: {due_date}")
        print(f"Product: {product}")
        print("-----------\n")

print(f"Total emails found with the specified keywords: {counter}")
