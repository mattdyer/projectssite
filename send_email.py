import smtplib
from email.mime.text import MIMEText

msg = MIMEText(
    "Project: Hangman\n"
    "Folder: docs/hangman/\n"
    "Progress: 18/60 projects completed (42 remaining)\n"
    "\n"
    "A classic letter-guessing game with canvas hangman drawing, 11 word categories, "
    "physical keyboard + touch/mouse support, score tracking.\n"
    "\n"
    "Commit: 1cb8bf1\n"
    "Pushed to: https://github.com/mattdyer/projectssite.git",
    'plain', 'utf-8'
)

msg['Subject'] = '[Project Builder] Hangman complete!'
msg['From'] = 'agent@md.mattdyer.us'
msg['To'] = 'madmatt1220@gmail.com'

with smtplib.SMTP_SSL('gcam1187.siteground.biz', 465) as s:
    s.login('agent@md.mattdyer.us', 'k1CR621b3#69')
    s.send_message(msg)

print('Email sent successfully')
