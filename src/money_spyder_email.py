import smtplib
import ssl
from email.message import EmailMessage

class MoneySpyderEmail:
    def SendLighthouseEmail(self, toAddress, stocks_to_observe):
        context = ssl.create_default_context()

        msg = EmailMessage()

        msg['Subject'] = "Money Spyder Lighthouse"
        msg['From'] = 'money.spyder.2020@gmail.com'
        msg['To'] = toAddress

        msg.set_content('Money Spyder Lighthouse recommends these stocks to look at.')

        msg.add_alternative(f"""
        <p>
            <h1>Money Spyder Lighthouse</h1>
            Money Spyder Lighthouse recommends these stocks to look at:<br><br>
            <strong>{stocks_to_observe}</strong>
        </p>
        """, subtype='html')

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()  # Say EHLO to server
            smtp.starttls(context=context)  # Puts the connection in TLS mode.
            smtp.ehlo()
            smtp.login(msg['From'], "BlackJack88")
            smtp.send_message(msg)
