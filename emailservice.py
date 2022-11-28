from email.message import EmailMessage
import ssl
import smtplib

email_sender = 'SENDER EMAIL'
email_password = 'PASSWORD OF SENDER EMAIL'
email_reciever = 'YOUR EMAIL'

wished_items = ['list wished characters here. Leave a space at the end! ']

# keep track of items already alerted
# when the OG listing disappears from the database, remove the item from alerted
alerteditems = open("alerteditems.txt", "r+")
alerted = alerteditems.readlines()

subject = 'PreOwnedPal: Pre-owned Listing Alert'
body = "The following listings match entries found on your wishlist:\n\n"

text = open("database.txt", "r")
listings = text.readlines()

i = 0
j = 0
k = 0
was_alerted = False
any_alerts = False

# go through the database and check for matching names
for line in listings:
    for item in wished_items:
        if (item in line):
            for alert in alerted:
                if alert == line:
                    was_alerted = True

            if (not was_alerted):
                body = body + line
                alerteditems.write(line + '\n')
                any_alerts = True
                j += 1

    if j == 1:
        j += 1
    elif j == 2:
        body = body + line
        j += 1
    elif j == 3:
        body = body + line + '\n'
        j = 0

    was_alerted = False
    i += 1

body = body + '\nThanks for using the PreOwnedPal service!'

if any_alerts:
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_reciever
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_reciever, em.as_string())

text.close()
