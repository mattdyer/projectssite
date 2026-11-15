import smtplib
from email.mime.text import MIMEText

msg = MIMEText(
    "Project: Gravity Drawing\n"
    "Folder: docs/gravity-drawing/index.html\n"
    "Progress: 39/61 projects completed (22 remaining)\n"
    "\n"
    "Draw strokes on canvas that fall with simulated gravity.\n"
    "Features brush size, gravity strength, trail controls, color picker,\n"
    "freeze mode, and particle bounce physics. Touch and mouse supported.",
    'plain', 'utf-8'
)

msg['Subject'] = '[Project Builder] Gravity Drawing complete!'
msg['From'] = 'agent@md.mattdyer.us'
msg['To'] = 'madmatt1220@gmail.com'

with smtplib.SMTP_SSL('gcam1187.siteground.biz', 465) as s:
    s.login('agent@md.mattdyer.us', 'k1CR621b3#69')
    s.send_message(msg)

print('Email sent successfully')
