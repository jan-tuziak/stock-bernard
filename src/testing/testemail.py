# import smtplib

# server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
# server.login("money.spyder.2020@gmail.com", "BlackJack88")
# toAddresses = ["jan.tuziak@outlook.com"]
# stocks_to_observe = 'NYSE:A,NYSE:AA,NASDAQ:AACQ,NASDAQ:AAL'
# message = f'Money Spyder recommends these stocks:\r\n{stocks_to_observe}'
# print(message)
# for mail in toAddresses:
#     server.sendmail("money.spyder.2020@gmail.com", mail, "NYSE:A,NYSE:AA,NASDAQ:AACQ,NASDAQ:AAL")
# server.quit()


import smtplib
import ssl
from email.message import EmailMessage

# Create a SSLContext object with default settings.
context = ssl.create_default_context()

msg = EmailMessage()

msg['Subject'] = "Money Spyder Lighthouse"
msg['From'] = 'money.spyder.2020@gmail.com'
msg['To'] = "jan.tuziak@outlook.com"

msg.set_content('Money Spyder Lighthouse recommends these stocks to look at.')

msg.add_alternative("""
<p>
    <h1>Money Spyder Lighthouse</h1>
    Money Spyder Lighthouse recommends these stocks to look at:<br><br>
    <strong>NYSE:A,NYSE:AA,NASDAQ:AACQ,NASDAQ:AAL</strong>
</p>
""", subtype='html')

with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()  # Say EHLO to server
    smtp.starttls(context=context)  # Puts the connection in TLS mode.
    smtp.ehlo()
    smtp.login(msg['From'], "BlackJack88")
    smtp.send_message(msg)