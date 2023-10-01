import imaplib
import email
import datetime

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
three_days_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime('%d-%b-%Y')
status, email_ids = mail.search(None, '(SINCE "' + three_days_ago + '")')

# Keywords to search for in the email subject
subject_keywords = ["bid", "request", "assignment"]

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

    # Check if the email subject contains the keywords
    if any(keyword.lower() in email_subject.lower() for keyword in subject_keywords):
        counter += 1
        print(f"Email {counter}:")
        print(f"From: {email_from}")
        print(f"Date Sent: {email_date}")
        print("-----------\n")

print(f"Total emails found with the specified keywords: {counter}")