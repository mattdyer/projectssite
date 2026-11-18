import smtplib
from email.mime.text import MIMEText

msg = MIMEText(
    "Project: Pomodoro Timer\n"
    "Folder: docs/pomodoro-timer/\n"
    "Progress: 48/61 projects completed (13 remaining)\n"
    "\n"
    "A 25-minute work / 5-minute break timer with:\n"
    "- Circular SVG progress ring\n"
    "- Animated particle background\n"
    "- Configurable durations via settings panel\n"
    "- Session tracking dots\n"
    "- Sound notifications\n"
    "- Keyboard shortcuts (Space=start/pause, R=reset)\n"
    "- Mobile/touch support\n"
    "- Auto-tab title updates with countdown"
)
msg['Subject'] = '[Project Builder] Pomodoro Timer complete!'
msg['From'] = 'agent@md.mattdyer.us'
msg['To'] = 'madmatt1220@gmail.com'

with smtplib.SMTP_SSL('gcam1187.siteground.biz', 465) as server:
    server.login('agent@md.mattdyer.us', 'k1CR621b3#69')
    server.send_message(msg)

print("Email sent successfully")