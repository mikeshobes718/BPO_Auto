import imaplib
import email
from bs4 import BeautifulSoup
<<<<<<< HEAD
=======
from collections import defaultdict
from datetime import datetime, timedelta
>>>>>>> 015fd82 (Renamed bpo1.py to bpogetter.py)

# Email credentials
EMAIL = 'bpo@unitedinvestmentsfirm.com'
PASSWORD = 'Bpos2020'
IMAP_SERVER = 'mail.unitedinvestmentsfirm.com'

def connect_to_email():
    # Connect to the mailbox using IMAP
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    
<<<<<<< HEAD
=======
    # Dictionary to store the count for each sender
    sender_count = defaultdict(int)
    
    # Calculate the date 3 days ago
    three_days_ago = datetime.now() - timedelta(days=3)
    date_str = three_days_ago.strftime('%d-%b-%Y')
    
>>>>>>> 015fd82 (Renamed bpo1.py to bpogetter.py)
    try:
        # Login to the mailbox
        mail.login(EMAIL, PASSWORD)
        print("Successfully connected to the email!")
        
        # Select the inbox (or any other mailbox if needed)
        mail.select('inbox')
        
<<<<<<< HEAD
        # Search for emails from voxtur with "New Assignment" in the subject
        status, email_ids = mail.search(None, '(FROM "voxtur")', '(SUBJECT "New Assignment")')
=======
        # Search for emails with specified subjects from the past 3 days
        search_criteria = f'(OR (OR (SUBJECT "bid") (SUBJECT "request")) (SUBJECT "assignment")) SINCE {date_str}'
        status, email_ids = mail.search(None, search_criteria)
>>>>>>> 015fd82 (Renamed bpo1.py to bpogetter.py)
        
        for e_id in email_ids[0].split():
            status, email_data = mail.fetch(e_id, '(RFC822)')
            raw_email = email_data[0][1]
            
            # Parse the raw email
            msg = email.message_from_bytes(raw_email)
            
<<<<<<< HEAD
            # Extract the email body
=======
            # Extract and print the email body
>>>>>>> 015fd82 (Renamed bpo1.py to bpogetter.py)
            email_body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/html":
                        email_body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
            else:
                email_body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            
<<<<<<< HEAD
            # Use BeautifulSoup to parse the HTML content
            soup = BeautifulSoup(email_body, 'html.parser')
            
            # Extract the desired information
            order_info = soup.find_all('td', style="border: 1px solid black; padding:8px")
            values = soup.find_all('td', style="border: 1px solid black; border-collapse:collapse")
            
            info_dict = {}
            for info, value in zip(order_info, values):
                key = info.get_text(strip=True)
                val = value.get_text(strip=True)
                info_dict[key] = val
            
            print(f"From: {msg['from']}")
            print(f"Product: {info_dict.get('Product:', 'N/A')}")
            print(f"Fee: {info_dict.get('Fee:', 'N/A')}")
            print(f"Due Date: {info_dict.get('Due Date:', 'N/A')}")
            print(f"Subject Address: {info_dict.get('Subject Address:', 'N/A')}")
            print("-----------\n")
        
=======
            sender = msg['from']
            sender_count[sender] += 1
            
            print(f"From: {sender}")
            print(f"Subject: {msg['subject']}")
            # print("Email Body:")
            # print(email_body)
            print("-----------\n")
        
        # Print the count for each sender
        print("Count for each sender:")
        for sender, count in sender_count.items():
            print(f"{sender}: {count} emails")
        
>>>>>>> 015fd82 (Renamed bpo1.py to bpogetter.py)
    except imaplib.IMAP4.error as e:
        print(f"Failed to connect to the email. Error: {e}")
    
    finally:
        # Logout and close the connection
        mail.logout()

if __name__ == "__main__":
    connect_to_email()
