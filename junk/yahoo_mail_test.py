import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


smtp_user = 'schat.app@yahoo.com'
smtp_password = 'owhqpqqllvgimobz' # app password
server = 'smtp.mail.yahoo.com'
port = 465
msg = MIMEMultipart("alternative")
msg["Subject"] = 'Why,Oh why!'
msg["From"] = smtp_user
msg["To"] = "nkowiredu002@st.ug.edu.gh"
msg.attach(MIMEText('\nsent via python', 'plain'))  
s = smtplib.SMTP_SSL(server, port)
s.ehlo()
s.login(smtp_user, smtp_password)
# s.sendmail(smtp_user, "nanakofiowiredu@gmail.com", msg.as_string())
s.send_message(msg)
s.quit()