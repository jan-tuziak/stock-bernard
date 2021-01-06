import smtplib
import ssl
import logging
from email.message import EmailMessage

class Postman:    
    def send_lh_email(self, toAddresses, stocks_to_observe):
        #Send Lighthouse email
        ms_mail = 'money.spyder.2020@gmail.com'
        ms_pass = "BlackJack88"

        logging.info('Creating Email')
        context = ssl.create_default_context()

        msg = EmailMessage()

        msg['Subject'] = "Lighthouse"
        msg['From'] = 'Money Spyder'
        msg['To'] = toAddresses

        msg.set_content("Money Spyder's Lighthouse recommends these stocks to look at.")

        email_body = f"""
        <p>
            <h1>Money Spyder's Lighthouse &#x1F4A1;</h1>
            Lighthouse recommends these stocks to look at:<br><br>
            <strong>{stocks_to_observe}</strong>
        </p>
        """
        msg.add_alternative(email_body, subtype='html')
        logging.debug(f"Email: {email_body}")

        logging.debug(f'Sending Emails from {ms_mail}')
        logging.info(f'Sending Emails to {toAddresses}')
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()  # Say EHLO to server
            smtp.starttls(context=context)  # Puts the connection in TLS mode.
            smtp.ehlo()
            smtp.login(ms_mail, ms_pass)
            smtp.send_message(msg)

if __name__ == "__main__":    
    logging.basicConfig(level=logging.DEBUG)
    pstm = Postman()
    addresses = ['jan.tuziak@outlook.com', 'jan.tuziak@gmail.com']
    pstm.send_lh_email(addresses, 'NYSE:AAPL')
