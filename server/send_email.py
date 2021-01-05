from queue import Queue
from threading import Thread
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import time
from constants import MAX_EMAIL_RETRIES


class SendEmail(Thread):
    """
    This class sends an email containing the activation code
    """

    def __init__(self):
        super().__init__(daemon=True)
        self.sender_email:str = "schat.app@yahoo.com"
        self.sender_password:str = "owhqpqqllvgimobz"
        self.sender_name:str = 'sChat'
        self.subject:str = 'Account Activation Code'
        self.recipient_email:str = ''
        self.activation_code:str = ''
        self.retries_count:int = 0
        self.email_queue:Queue = Queue()
        self.stop:bool = False

    def add_to_queue(self, email_address:str, activation_code:str) -> None:
        """
        Adds message to the queue
        """
        self.email_queue.put((email_address, activation_code))

    def send_email(self) -> None:
        """
        Sends the email
        """
        try:
            # create message
            msg:MIMEMultipart = MIMEMultipart("alternative")
            msg["Subject"] = self.subject
            msg["From"] = formataddr((self.sender_name, self.sender_email))
            msg["To"] = self.recipient_email
            content:str = f'<html><h1><strong>ACTIVATION CODE: <span style="color: green">{self.activation_code}</span> </strong></h1>'
            msg.attach(MIMEText(content, 'html'))  
            # connect to mail server and login
            smtp:smtplib.SMTP_SSL = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)
            smtp.ehlo()
            smtp.login(self.sender_email, self.sender_password)
            # send the message
            smtp.send_message(msg)
            # close the connection
            smtp.quit()
        except Exception as e:
            print(e)
            if self.retries_count < MAX_EMAIL_RETRIES:
                self.retries_count += 1
                time.sleep(5)
                self.send_email()

    def run(self):
        """
        This method runs the email thread
        """
        while not self.stop:
            if not self.email_queue.empty():
                queue_data:tuple = self.email_queue.get()
                self.recipient_email:str = queue_data[0]
                self.activation_code:str = queue_data[1]
                self.send_email()
            

