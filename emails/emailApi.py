import smtplib
from email.message import EmailMessage
import requests
from io import BytesIO

class EmailAPI():
    def __init__(self, ) -> None:
        pass

    def send_mail(self, sender_email, reciever_email, password, email_subject, email_msg, msg_attach):
        print(sender_email)
        print(reciever_email)
        print(password)
        print(email_subject)
        print(email_msg)
        print(msg_attach)
        Sender_Email = sender_email
        Reciever_Email = reciever_email
        Password = password

        newMessage = EmailMessage()    
        newMessage['Subject'] = email_subject
        newMessage['From'] = Sender_Email  
        newMessage['To'] = Reciever_Email

        # Email body content
        newMessage = self.send_text_msg(newMessage, email_msg)

        # Email attach
        if len(msg_attach) > 0:
            for msg in msg_attach:
                if msg['type'] == "Text":
                    newMessage = self.send_text_msg(newMessage, msg['content'])
                if msg['type'] == "Image":
                    newMessage = self.send_image_msg(newMessage, msg['content'])
                if msg['type'] == "Video":
                    newMessage = self.send_video_msg(newMessage, msg['content'])
                if msg['type'] == "PDF":
                    newMessage = self.send_file_msg(newMessage, msg['content'])


        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(Sender_Email, Password) 
            smtp.send_message(newMessage)
        
        
        print("EMAI SENT!")
    

    def send_text_msg(self, content, text):
        content.set_content(text)
        return content

    def send_image_msg(self, content, text):
        response = requests.get(text)
        img = BytesIO(response.content)
        content.add_attachment(img.getvalue(), maintype='image', subtype="jpg", filename="image.jpg")
        return content
    

    def send_file_msg(self, content, text):
        response = requests.get(text)
        file = BytesIO(response.content)
        content.add_attachment(file.getvalue(), maintype='application', subtype="octet-stream", filename="file.pdf")
        return content
    
    def send_video_msg(self, content, text):
        response = requests.get(text)
        video = BytesIO(response.content)
        content.add_attachment(video.getvalue(), maintype='video', subtype="mp4", filename="file.mp4")
        return content




# https://www.codeitbro.com/send-email-using-python/


# https://www.asx.com.au/asxpdf/20171108/pdf/43p1l61zf2yct8.pdf
# https://tinypng.com/images/social/website.jpg
