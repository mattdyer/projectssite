import smtplib
from email.mime.text import MIMEText

msg = MIMEText(
    "Project: Breathing Exercise\n"
    "Folder: docs/breathing-exercise/\n"
    "Progress: 50/61 projects completed (11 remaining)\n"
    "\n"
    "Animated guided breathing app with 4 techniques (4-7-8, Box, Calm, Coherent), expanding/contracting circle animation, particle effects, and mobile touch support.",
    'plain', 'utf-8'
)

msg['Subject'] = '[Project Builder] Breathing Exercise complete!'
msg['From'] = 'agent@md.mattdyer.us'
msg['To'] = 'madmatt1220@gmail.com'

with smtplib.SMTP_SSL('gcam1187.siteground.biz', 465) as s:
    s.login('agent@md.mattdyer.us', 'k1CR621b3#69')
    s.send_message(msg)

print('Email sent successfully')
