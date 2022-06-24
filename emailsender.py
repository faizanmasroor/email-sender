import os
import imghdr
from email.message import EmailMessage
import smtplib

# make sure to define env variables for the sender email and sender password in order for the program to work

address = os.environ.get('sender_mail')
password = os.environ.get('sender_pass')
msg = EmailMessage()


def create_email(recipient):
    msg['Subject'] = input("\nPlease type the subject of the email.\n\n")
    msg['From'] = address
    msg['To'] = recipient
    body = input("\nPlease type the body of the email.\n\n")
    msg.set_content(body)


def add_image():
    try:
        file_name = input("\nWhat is the name of the file with the extension? (ex. image.png, picture.jpg)\n\n")
        with open(file_name, 'rb') as f:
            img_data = f.read()
            img_type = imghdr.what(f.name)
            img_name = f.name
            msg.add_attachment(img_data, maintype='image', subtype=img_type, filename=img_name)
    except FileNotFoundError:
        print("\nThe file you typed does not exist.")
        quit()


def send_email():
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(address, password)
            smtp.send_message(msg)
    except smtplib.SMTPAuthenticationError:
        print("You gave the incorrect login information for your gmail account.")
        quit()
    except smtplib.SMTPRecipientsRefused:
        print("The email address which you wish to email does not exist.")
        quit()


if __name__ == "__main__":
    target = input("Who will receive the email? (ex. johndoe@gmail.com)\n\n")
    create_email(target)
    is_attachment = input("Would you like to attach an image to the email? (Type yes or press enter to skip.)\n\n")
    if is_attachment == "yes":
        add_image()
    send_email()
    print("Email sent!")
