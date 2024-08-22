import glob
import os
import smtplib
from PIL import Image
from io import BytesIO
from email.message import EmailMessage

PASSWORD = os.getenv("PASSWORD")
SENDER = "yehor.kosiachkin@gmail.com"
RECEIVER = "yehor.kosiachkin@gmail.com"


def send_email(image_path):
    print("send_email function started")
    email_message = EmailMessage()
    email_message["Subject"] = "New camera alert!"
    email_message.set_content("Hey, it is a new alert of an object")

    with open(image_path, "rb") as file:
        content = file.read()
        filename = file.name
        im_data = BytesIO(content)
        im = Image.open(im_data)
        im_type = im.format

    email_message.add_attachment(content,
                                 maintype="image",
                                 subtype=im_type,
                                 filename=filename)

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()
    print("send_email function ended")


def clean_folder():
    print("clean_folder function started")
    images = glob.glob("images\\*.png")
    for image in images:
        os.remove(image)
    print("clean_folder function ended")


if __name__ == "__main__":
    send_email(image_path="images\\19.png")
