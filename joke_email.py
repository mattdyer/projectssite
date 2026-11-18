import smtplib
from email.mime.text import MIMEText

msg = MIMEText(
    "Project: Joke of the Day\n"
    "Folder: docs/joke-of-the-day/\n"
    "Progress: 47/61 projects completed (14 remaining)\n"
    "\n"
    "Interactive joke fetcher powered by JokeAPI with category filtering (Programming, Pun, Spooky, Christmas, Dark, Knock Knock), twinkling star background, emoji burst animations, punchline reveal transitions, swipe/tap support, and a responsive dark theme.",
    'plain', 'utf-8'
)

msg['Subject'] = '[Project Builder] Joke of the Day complete!'
msg['From'] = 'agent@md.mattdyer.us'
msg['To'] = 'madmatt1220@gmail.com'

with smtplib.SMTP_SSL('gcam1187.siteground.biz', 465) as s:
    s.login('agent@md.mattdyer.us', 'k1CR621b3#69')
    s.send_message(msg)

print('Email sent successfully')
