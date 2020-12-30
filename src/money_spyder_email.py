import smtplib
import ssl
from email.message import EmailMessage

class MoneySpyderEmail:
    def __init__(self, printToConsole=False):
        self.printToConsole = printToConsole
    
    def SendLighthouseEmail(self, toAddress, stocks_to_observe):
        self.print('Creating Email... ')
        context = ssl.create_default_context()

        msg = EmailMessage()

        msg['Subject'] = "Money Spyder's Lighthouse;"
        msg['From'] = 'money.spyder.2020@gmail.com'
        msg['To'] = toAddress

        msg.set_content("Money Spyder's Lighthouse recommends these stocks to look at.")

        msg.add_alternative(f"""
        <p>
            <h1>Money Spyder's Lighthouse &#x1F4A1;</h1>
            Money Spyder Lighthouse recommends these stocks to look at:<br><br>
            <strong>{stocks_to_observe}</strong>
        </p>
        """, subtype='html')

        self.print('Sending Emails... ')
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()  # Say EHLO to server
            smtp.starttls(context=context)  # Puts the connection in TLS mode.
            smtp.ehlo()
            smtp.login(msg['From'], "BlackJack88")
            smtp.send_message(msg)

    def print(self, msg, end='\r\n'):
        if self.printToConsole: print(f'MoneySpyderEmail::{msg}', end=end)

if __name__ == "__main__":    
    msEmail = MoneySpyderEmail(printToConsole=True)
    msEmail.SendLighthouseEmail('jan.tuziak@outlook.com', 'NYSE:AAPL')