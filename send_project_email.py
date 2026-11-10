#!/usr/bin/env python3
import smtplib, ssl
from email.mime.text import MIMEText

msg = MIMEText(
    "Project: Simon Says\n"
    "Folder: docs/simon-says/index.html\n"
    "Progress: 14/60 projects complete\n"
    "\n"
    "A sequence memory game where players watch a growing pattern of colored buttons with tones and must repeat it back. Features audio tones, touch support, persistent high scores, and increasing speed."
)
msg['Subject'] = '[Project Builder] Simon Says complete!'
msg['From'] = 'agent@md.mattdyer.us'
msg['To'] = 'madmatt1220@gmail.com'

context = ssl.create_default_context()
with smtplib.SMTP_SSL('gcam1187.siteground.biz', 465, context=context) as server:
    server.login('agent@md.mattdyer.us', 'k1CR621b3#69')
    server.sendmail('agent@md.mattdyer.us', 'madmatt1220@gmail.com', msg.as_string())

print("Email sent successfully.")