import smtplib
from email.mime.text import MIMEText

msg = MIMEText(
    "Project: Waveform Synth\n"
    "Folder: docs/waveform-synth/\n"
    "Progress: 33/60 projects completed (27 remaining)\n"
    "\n"
    "A draw-and-hear waveform generator using the Web Audio API. Users draw a waveform shape on the canvas, then hear it synthesized as sound with adjustable frequency and volume. Includes preset waveforms (sine, square, sawtooth, triangle), smooth/edge rendering, live audio visualization with frequency bars, and full touch/mobile support.\n"
    "\n"
    "Commit: faddb51\n"
    "Pushed to: https://github.com/mattdyer/projectssite.git",
    'plain', 'utf-8'
)

msg['Subject'] = '[Project Builder] Waveform Synth complete!'
msg['From'] = 'agent@md.mattdyer.us'
msg['To'] = 'madmatt1220@gmail.com'

with smtplib.SMTP_SSL('gcam1187.siteground.biz', 465) as s:
    s.login('agent@md.mattdyer.us', 'k1CR621b3#69')
    s.send_message(msg)

print('Email sent successfully')
