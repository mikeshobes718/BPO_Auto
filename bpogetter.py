import imaplib
import email
import re
import datetime

# Your email credentials
EMAIL = 'careersglobal@unitedinvestmentsfirm.com'
EMAIL = 'bpo@unitedinvestmentsfirm.com'
EMAIL = 'bpos@unitedinvestmentsfirm.com'
PASSWORD = 'Bpos2020'
IMAP_SERVER = 'mail.unitedinvestmentsfirm.com'

# Connect to your mailbox using IMAP
try:
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')
except imaplib.IMAP4.error as e:
    if "AUTHENTICATIONFAILED" in str(e):
        print("Authentication failed. Please check your email and password.")
    else:
        print(f"An IMAP error occurred: {e}")
    exit(1)
except ConnectionRefusedError:
    print("Error: Unable to connect to the IMAP server. Please check the server address and port.")
    exit(1)

# Search for emails from the past 2 days, including today
two_days_ago = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%d-%b-%Y')
status, email_ids = mail.search(None, '(SINCE "' + two_days_ago + '")')

# Debug print: Print the status and number of email IDs retrieved
print(f"Search status: {status}")
print(f"Number of emails retrieved: {len(email_ids[0].split())}")

# Check if there are no emails from the past 2 days
if not email_ids or not email_ids[0]:
    print("No emails found from the past 2 days.")
    exit(0)

# Keywords and regex patterns to search for
keywords = ["bpo", "fee", "Bid", "assignment"]
fee_bid_pattern = re.compile(r'(fee|bid):\s*\$\s*(\d+(\.\d{2})?)', re.IGNORECASE)

# Iterate through all emails and add a debug print for each email processed
for e_id in email_ids[0].split():
    print(f"Processing email ID: {e_id.decode('utf-8')}")
    
    status, email_data = mail.fetch(e_id, '(RFC822)')
    raw_email = email_data[0][1]

    # Parse the raw email
    msg = email.message_from_bytes(raw_email)
    email_from = msg['from']
    email_date = msg['date']
    email_body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            match content_type:
                case "text/plain" if "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                        email_body += body
                    except:
                        pass
    else:
        email_body += msg.get_payload(decode=True).decode('utf-8', errors='replace')

    # Check if the email body contains fee or bid amount
    match = fee_bid_pattern.search(email_body)
    if match:
        amount_type = match.group(1)
        amount = match.group(2)
        print(f"From: {email_from}")
        print(f"Date Sent: {email_date}")
        print(f"{amount_type.capitalize()}: ${amount}\n\n")
