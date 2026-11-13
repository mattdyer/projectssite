import smtplib
from email.mime.text import MIMEText

msg = MIMEText(
    "Project: Kaleidoscope\n"
    "Folder: docs/kaleidoscope/\n"
    "Progress: 30/60 projects completed (30 remaining)\n"
    "\n"
    "An interactive kaleidoscope art tool where users draw or drag on a canvas to create\n"
    "symmetric mirror patterns. Features include configurable symmetry (2-20 segments),\n"
    "adjustable brush size, a curated color palette, custom background color, rainbow\n"
    "animation mode, and PNG image export. Full touch support for mobile devices.\n"
    "\n"
    "Commit: 298fb51\n"
    "Pushed to: https://github.com/mattdyer/projectssite.git",
    'plain', 'utf-8'
)

msg['Subject'] = '[Project Builder] Kaleidoscope complete!'
msg['From'] = 'agent@md.mattdyer.us'
msg['To'] = 'madmatt1220@gmail.com'

with smtplib.SMTP_SSL('gcam1187.siteground.biz', 465) as s:
    s.login('agent@md.mattdyer.us', 'k1CR621b3#69')
    s.send_message(msg)

print('Email sent successfully')
