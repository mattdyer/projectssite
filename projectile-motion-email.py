import smtplib
from email.mime.text import MIMEText

msg = MIMEText('''Project: Projectile Motion
Folder: docs/projectile-motion/

Progress: 52/61 projects completed (9 remaining)

The Projectile Motion simulator features:
- Adjustable launch angle (5-85 degrees)
- Adjustable initial speed (5-50 m/s)
- Adjustable gravity (1-20 m/s²)
- Adjustable launch height (0-100 m)
- Real-time trajectory tracking with optional trail
- Target scoring mode (toggle on/off)
- Live stats: distance, max height, flight time, speed, height
- Starfield background with ground and grid
- Responsive/mobile-friendly canvas

Files changed:
- docs/projectile-motion/index.html (new)
- docs/index.htm (link added)
- PROJECT-IDEAS.md (marked as done)

Commit: be38518
Pushed: origin/master
''', 'plain')

msg['Subject'] = '[Project Builder] Projectile Motion complete!'
msg['From'] = 'agent@md.mattdyer.us'
msg['To'] = 'madmatt1220@gmail.com'

with smtplib.SMTP_SSL('gcam1187.siteground.biz', 465) as s:
    s.login('agent@md.mattdyer.us', 'k1CR621b3#69')
    s.sendmail('agent@md.mattdyer.us', 'madmatt1220@gmail.com', msg.as_string())

print('Email sent successfully')
