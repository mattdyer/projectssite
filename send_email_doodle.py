import smtplib
from email.mime.text import MIMEText

msg = MIMEText(
    "Project: Doodle Jump\nFolder: docs/doodle-jump/\nProgress: 13/60 projects completed"
)
msg['Subject'] = '[Project Builder] Doodle Jump complete!'
msg['From'] = 'agent@md.mattdyer.us'
msg['To'] = 'madmatt1220@gmail.com'

with smtplib.SMTP_SSL('gcam1187.siteground.biz', 465) as server:
    server.login('agent@md.mattdyer.us', 'k1CR621b3#69')
    server.sendmail('agent@md.mattdyer.us', 'madmatt1220@gmail.com', msg.as_string())
print('Email sent successfully')
