import os
from dotenv import load_dotenv
import smtplib

load_dotenv()

class NotificationManager:
    def __init__(self) -> None:
        self._email = os.environ["My_Email"]
        self._password = os.environ["Email_Password"]
        
    def send_message(self, message):
        '''
        Sends an email when the price of a flight dips below the lowest price.
        
        Parameters:
        message (str): the body of the email
        
        Returns:
        None
        '''
        
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=self._email, password=self._password)
            connection.sendmail(from_addr=self._email, to_addrs=os.environ["To_Email"], msg=message)