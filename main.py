"""In order for this program to function, you will preferably create another dummy Gmail account and enable 2FA and app
passwords in Google Account settings. After creating an app you will receive a 16-digit password which is what you will
set SENDER_PASS equal to in your .env file."""

import os
from email.message import EmailMessage
import imghdr
import smtplib

# gets the address and password for the sender email
print(os.environ['SENDER_PASS'])
quit()


def create_email(target, subject, body) -> EmailMessage:
    """Adds the
    subject
    from, to, and body attributes to the email message"""

    msg = EmailMessage()
    msg['To'] = target
    msg['Subject'] = subject
    msg['From'] = sender_mail
    msg.set_content(body)

    return msg


def add_image(msg: EmailMessage):
    """Prompts the user to enter an image name and proceeds to append it to the existing email message
    Image data must be read in read-binary,
    The full image name is needed, such as image.jpg, and it must be within the project directory."""

    try:
        file_name = input("Type the image's full name (ex. image.png, picture.jpg): ")
        with open(file_name, 'rb') as f:
            img_data = f.read()
            img_type = imghdr.what(f.name)
            img_name = f.name

            msg.add_attachment(img_data, maintype='image', subtype=img_type, filename=img_name)

    except FileNotFoundError:
        print("\nThe file you typed does not exist.")
        quit()


def send_email(msg: EmailMessage, spam=False, thread=None):
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

        if not spam:
            print("\nEmail has been sent.")
        if spam:
            print(f"Email {thread + 1} has been sent.")

        server.quit()

    except smtplib.SMTPAuthenticationError:
        print("\nYou gave the incorrect login information for your gmail account.")
        quit()
    except smtplib.SMTPRecipientsRefused:
        print("\nThe email address which you wish to email does not exist.")
        quit()


def main():
    mail_target = input("Type the recipient of your email (ex. 'johndoe@gmail.com'): ")
    mail_subject = input("Type the the subject of your email: ")
    mail_body = input("Type the body of your email:\n")

    email = create_email(mail_target, mail_subject, mail_body)

    is_attachment = input("\nWould you like to attach an image to the email? [y/n]: ")
    if is_attachment == "y":
        add_image(email)

    send_email(email)


if __name__ == "__main__":
    main()
