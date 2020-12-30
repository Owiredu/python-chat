from threading import Thread
import smtplib
from email.message import EmailMessage
from email.headerregistry import Address


class SendEmail(Thread):
    """
    This class sends an email containing the activation code
    """

    def __init__(self):
        super().__init__()
        self.sender_email = "unibasesoftware@gmail.com"
        self.sender_password = "Godisgood2018"
        self.sender_name = 'sChat'
        self.subject = 'Account Activation Code'

    def create_smtp_connection(self):
        """
        This method creates the smtp connection
        """
        # create connection
        self.smtp = smtplib.SMTP('smtp.gmail.com', 587, 'localhost')
        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.login(self.sender_email, self.sender_password)

    def set_email_info(self, recipient_email, activation_code):
        # argument types: String, String, list
        """
        This method sets the recognition info
        """
        self.recipient_email = recipient_email
        self.activation_code = activation_code

    def set_subject_sender_recipient(self):
        """
        This method set the subject, sender and recipient emails
        """
        # create the message holder
        self.message = EmailMessage()
        self.message['Subject'] = self.subject
        self.message['From'] = Address(self.sender_name, '', self.sender_email)
        self.message['To'] = self.recipient_email

    def set_msg_content(self):
        """
        This method sets the content of the email
        """
        self.message.set_content('')
        content = f'<html><h1><strong>ACTIVATION CODE: <span style="color: green">{self.activation_code}</span> </strong></h1>'
        self.message.add_alternative(content, subtype='html')

    def smtp_send_message(self):
        """
        This method sends the message
        """
        self.smtp.send_message(self.message)

    def close_smtp(self):
        """
        This method closes the smtp server
        """
        self.smtp.quit()

    def send_email(self):
        """
        Sends the email
        """
        self.create_smtp_connection()
        self.set_subject_sender_recipient()
        self.set_msg_content()
        self.smtp_send_message()
        self.close_smtp()

    def run(self):
        """
        This method sends the alert
        """
        try:
            self.send_email()
        except:
            self.send_email()
            

