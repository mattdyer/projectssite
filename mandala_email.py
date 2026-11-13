import smtplib
from email.mime.text import MIMEText

msg = MIMEText(
    "Project: Mandala Generator\n"
    "Folder: docs/mandala-generator/\n"
    "Progress: 29/59 projects completed\n"
    "\n"
    "A symmetrical art tool where drawing one stroke mirrors across N axes. "
    "Features include adjustable symmetry (2–24 axes), brush size, color picker, "
    "three rendering styles (Solid, Neon Glow, Dotted), undo, clear, and PNG export. "
    "Fully touch-friendly for mobile drawing.\n"
    "\n"
    "Commit: 3fd703f\n"
    "Pushed to: https://github.com/mattdyer/projectssite.git",
    'plain', 'utf-8'
)

msg['Subject'] = '[Project Builder] Mandala Generator complete!'
msg['From'] = 'agent@md.mattdyer.us'
msg['To'] = 'madmatt1220@gmail.com'

with smtplib.SMTP_SSL('gcam1187.siteground.biz', 465) as s:
    s.login('agent@md.mattdyer.us', 'k1CR621b3#69')
    s.send_message(msg)

print('Email sent successfully')
