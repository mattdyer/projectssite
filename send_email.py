import smtplib
from email.mime.text import MIMEText

msg = MIMEText(
    "Project: Number Guessing Game\n"
    "Folder: docs/number-guessing-game/\n"
    "Progress: 43/61 projects completed (18 remaining)\n"
    "\n"
    "Interactive number guessing game with 3 difficulty levels, attempt tracking, localStorage best scores, color-coded guess history, and confetti celebration.",
    'plain', 'utf-8'
)

msg['Subject'] = '[Project Builder] Number Guessing Game complete!'
msg['From'] = 'agent@md.mattdyer.us'
msg['To'] = 'madmatt1220@gmail.com'

with smtplib.SMTP_SSL('gcam1187.siteground.biz', 465) as s:
    s.login('agent@md.mattdyer.us', 'k1CR621b3#69')
    s.send_message(msg)

print('Email sent successfully')
