import smtplib
from email.mime.text import MIMEText

msg = MIMEText(
    "Project: Dice Roller\n"
    "Folder: docs/dice-roller/\n"
    "Progress: 26/62 projects completed (36 remaining)\n"
    "\n"
    "An interactive dice roller where users configure dice count (1-10) and sides "
    "(D4, D6, D8, D10, D12, D20, D100). Features include animated 3D rolling, "
    "hot/cold roll feedback, roll history with stats (avg/max), keyboard and touch "
    "support, and mobile-responsive layout.\n"
    "\n"
    "Commit: 91ea403\n"
    "Pushed to: https://github.com/mattdyer/projectssite.git",
    'plain', 'utf-8'
)

msg['Subject'] = '[Project Builder] Dice Roller complete!'
msg['From'] = 'agent@md.mattdyer.us'
msg['To'] = 'madmatt1220@gmail.com'

with smtplib.SMTP_SSL('gcam1187.siteground.biz', 465) as s:
    s.login('agent@md.mattdyer.us', 'k1CR621b3#69')
    s.send_message(msg)

print('Email sent successfully')
