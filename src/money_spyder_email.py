import smtplib
import ssl
import logging
from email.message import EmailMessage

class MoneySpyderEmail:    
    def send_lh_email(self, toAddress, stocks_to_observe):
        #Send Lighthouse email
        logging.info('Creating Email')
        context = ssl.create_default_context()

        msg = EmailMessage()

        msg['Subject'] = "Money Spyder's Lighthouse;"
        msg['From'] = 'money.spyder.2020@gmail.com'
        msg['To'] = toAddress

        msg.set_content("Money Spyder's Lighthouse recommends these stocks to look at.")

        email_body = f"""
        <p>
            <h1>Money Spyder's Lighthouse &#x1F4A1;</h1>
            Money Spyder Lighthouse recommends these stocks to look at:<br><br>
            <strong>{stocks_to_observe}</strong>
        </p>
        """
        msg.add_alternative(email_body, subtype='html')
        logging.debug(f"Email: {email_body}")

        logging.info('Sending Emails')
        logging.debug(f'Sending Emails from {msg["From"]}')
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()  # Say EHLO to server
            smtp.starttls(context=context)  # Puts the connection in TLS mode.
            smtp.ehlo()
            smtp.login(msg['From'], "BlackJack88")
            smtp.send_message(msg)

if __name__ == "__main__":    
    logging.basicConfig(level=logging.DEBUG)
    msEmail = MoneySpyderEmail()
    msEmail.send_lh_email('jan.tuziak@outlook.com', 'NYSE:AAPL')
