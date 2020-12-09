#!/bin/env python3

from abuse_finder import domain_abuse
import sys
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from defang import defang



company_name = "Dunder Mifflin"
abuse_contact = "abuse@google.com"

def getAbuse(domain):
    abuse_email = domain_abuse(domain)

    return abuse_email['abuse']

def send_report(abuseContact:str,domain:str):
    port = 465  # For starttls
    smtp_server = "smtp.google.com"
    sender_email = "abuse@org.com""
    receiver_email = abuse_email
    password = input("Type your email password and press enter: ")

    message = MIMEMultipart("alternative")
    message["Subject"] = "ABUSE COMPLAINT FROM " + company_name + "!""
    message["From"] = sender_email
    message["To"] = receiver_email
    
    text = """\
    This is a message sent from """ + company_name + """\'s Security team.
    
    The following domain you are the registrar for (""" + defang(domain) + """) is 
    being used for malicious attacks infringing on our intellectual property,
    or is being used for conducting phishing attacks to our suppliers.
    
    Please do the needful and take this domain down.  If you require further information
    or further proof of malicious usage, please respond to """ + abuse_contact + """.
    
    This email is originating from a non-monitored mailbox."""
    html = """\
    <html>
        <body>
            <p>
                <h5>
                    This is a message sent from """ + company_name + """\'s Security team.<br>
                </h5>
                <br>
                The following domain you are the registrar for (<b>""" + defang(domain) + """</b>) is 
                being used for malicious attacks infringing on our intellectual property,
                or is being used for conducting phishing attacks to our suppliers.
                <br>
                Please do the needful and take this domain down.
                <br>
                If you require further information or further proof of malicious usage, 
                please respond to <a href="mailto:""" + abuse_contact + """ \">""" + abuse_contact + """</a>.<br>
                <br>
                This email is originating from a non-monitored mailbox.<br>
            </p>
        </body>
    </html>     
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context = context) as server:
        server.login(sender_email, password)
	server.ehlo()  # Can be omitted
        server.sendmail(sender_email, receiver_email, message.as_string())


def main():
    domain = sys.argv[1]
    abuse_email = getAbuse(domain)
    print(abuse_email)
    send_report(abuse_email,domain)

if __name__ == "__main__":
    main()
