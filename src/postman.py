import smtplib
import ssl
import logging
from email.message import EmailMessage

class Postman:
    def __init__(self, mail, password, to_addresses):
        self.mail = mail
        self.password = password
        self.to_addresses = to_addresses

    def send_lh_email(self, stocks_to_observe, criterias):
        #Send Lighthouse email
        crt = '<br>- '.join(criterias)
        crt = '- ' + crt
        
        logging.info('Creating Email')
        context = ssl.create_default_context()

        msg = EmailMessage()

        msg['Subject'] = "Lighthouse"
        msg['From'] = 'Money Spyder'
        msg['To'] = self.to_addresses

        msg.set_content("Money Spyder's Lighthouse recommends these stocks to look at.")

        email_body = f"""
        <p>
            <h1>Money Spyder's Lighthouse &#x1F4A1;</h1>
            <h2>Criterias</h2><br>{crt}<br><br><h2>Stocks</h2><br>
            <strong>{stocks_to_observe}</strong>
        </p>
        """
        msg.add_alternative(email_body, subtype='html')
        logging.debug(f"Email: {email_body}")

        logging.debug(f'Sending Emails from {self.mail}')
        logging.info(f'Sending Emails to {self.to_addresses}')
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()  # Say EHLO to server
            smtp.starttls(context=context)  # Puts the connection in TLS mode.
            smtp.ehlo()
            smtp.login(self.mail, self.password)
            smtp.send_message(msg)

if __name__ == "__main__":    
    logging.basicConfig(level=logging.DEBUG)
    pstm = Postman('money.spyder.2020@gmail.com','BlackJack88', 'jan.tuziak@gmail.com')
    pstm.send_lh_email('NYSE:AAPL', ['daily turnover > $10mln', 'sma300x15min > sma100x15min', 'sma30x15min > sma100x15min'])
