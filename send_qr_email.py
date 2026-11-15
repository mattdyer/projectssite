import smtplib, ssl
from email.message import EmailMessage

msg = EmailMessage()
msg['From'] = 'agent@md.mattdyer.us'
msg['To'] = 'madmatt1220@gmail.com'
msg['Subject'] = '[Project Builder] QR Code Generator complete!'
body = '''Project: QR Code Generator
Folder: docs/qr-code-generator/
Progress: 34/61 done

A QR Code Generator has been built — type text or a URL and get an instant downloadable QR code, all in-browser with no backend required.
'''
msg.set_content(body)

context = ssl.create_default_context()
with smtplib.SMTP_SSL('gcam1187.siteground.biz', 465, context=context) as server:
    server.login('agent@md.mattdyer.us', 'k1CR621b3#69')
    server.send_message(msg)
print('Email sent successfully.')
