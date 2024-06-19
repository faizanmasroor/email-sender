"""Refer to README.md before using this program."""

from email.message import EmailMessage
from os import environ

import imghdr
import smtplib

sender_mail = environ['SENDER_MAIL']
sender_pass = environ['SENDER_PASS']


# Creates an EmailMessage object with the basic elements of an email
def create_email(recipient, subject, body) -> EmailMessage:
    msg = EmailMessage()
    msg['To'] = recipient
    msg['Subject'] = subject
    msg['From'] = sender_mail
    msg.set_content(body)

    return msg


# If the user wants to add an image, this function is called; it asks for the  # TODO: Finish comment
def add_image(msg: EmailMessage):
    """Prompts the user to enter an image name and proceeds to append it to the existing email message
    Image data must be read in read-binary,
    The full image name is needed, such as image.jpg, and it must be within the project directory."""
    try:
        file_name = input("Type the image's full name with its relative location of the script (ex. image.png,"
                          "picture.jpg, ../../graph.svg, ../MyPhotos/dog.png, etc): ")
        with open(file_name, 'rb') as f:
            img_data = f.read()
            img_type = imghdr.what(f.name)
            img_name = f.name

            msg.add_attachment(img_data, maintype='image', subtype=img_type, filename=img_name)

        print("\nImage successfully added.")

    except FileNotFoundError:
        print("\nThe file you typed does not exist.")


def send_email(msg: EmailMessage):
    """This function:
    connects to an SMTP server,
    encrypts message with TLS,
    logs into the sender's Gmail,
    sends email message (which has Subject, From, To, Body),

    spam and thread parameters are only set to True and int when:
    the spam() function is called and Thread() instances offset these args"""

    try:
        server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_mail, sender_pass)
        server.send_message(msg)

        print("\nEmail has been sent.")

        server.quit()

    except smtplib.SMTPAuthenticationError:
        print("\nYou gave the incorrect login information for your gmail account.")
        quit()
    except smtplib.SMTPRecipientsRefused:
        print("\nThe email address which you wish to email does not exist.")
        quit()


def main():
    mail_recipient = input("Type the recipient of your email (ex. 'johndoe@gmail.com'): ")
    mail_subject = input("Type the the subject of your email: ")
    mail_body = input("Type the body of your email:\n")

    email = create_email(mail_recipient, mail_subject, mail_body)

    while True:
        is_attachment = input("\nWould you like to attach an image to the email? [y/n]: ")
        if is_attachment == "y":
            add_image(email)
            continue
        break

    send_email(email)


if __name__ == "__main__":
    main()
