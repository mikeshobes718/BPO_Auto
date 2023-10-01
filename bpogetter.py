import imaplib
import email
import re
import datetime  # <-- Added this import

# Your email credentials
EMAIL = 'careersglobal@unitedinvestmentsfirm.com'
EMAIL = 'bpo@unitedinvestmentsfirm.com'
PASSWORD = 'Bpos2020'
IMAP_SERVER = 'mail.unitedinvestmentsfirm.com'

# Connect to your mailbox using IMAP
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)
mail.select('inbox')

# Search for emails from the past 2 days, including today
two_days_ago = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%d-%b-%Y')
status, email_ids = mail.search(None, '(SINCE "' + two_days_ago + '")')  # <-- Updated this line

# Keywords and regex patterns to search for
keywords = ["bpo", "fee", "Bid", "assignment"]
fee_bid_pattern = re.compile(r'(fee|bid):\s*\$\s*(\d+(\.\d{2})?)', re.IGNORECASE)

# Iterate through all emails
for e_id in email_ids:
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
