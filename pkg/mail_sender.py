import smtplib





class MailSender:
    
    def __init__(self, sender_mail, token,
                 mail_server="smtp.gmail.com", port=587):
        
        self.sender_mail = sender_mail
        self.token = token
        self.mail_server = mail_server
        self.port = port

    def send_message(self, message, receiver):
        with smtplib.SMTP(self.mail_server, self.port) as connection:  
            connection.starttls()  
            connection.login(self.sender_mail, password=self.token)  
            connection.sendmail(from_addr=self.sender_mail,  
                                to_addrs=receiver,  
                                msg=f"Subject:Blog Project\n\n{message}")
    