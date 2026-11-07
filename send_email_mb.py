import smtplib
from email.mime.text import MIMEText

msg = MIMEText(
    "Project: Memory Match\nFolder: docs/memory-match/\nProgress: 9/60 projects completed (51 remaining)"
)
msg['Subject'] = '[Project Builder] Memory Match complete!'
msg['From'] = 'agent@md.mattdyer.us'
msg['To'] = 'madmatt1220@gmail.com'

with smtplib.SMTP_SSL('gcam1187.siteground.biz', 465) as server:
    server.login('agent@md.mattdyer.us', 'k1CR621b3#69')
    server.sendmail('agent@md.mattdyer.us', 'madmatt1220@gmail.com', msg.as_string())
print('Email sent successfully')