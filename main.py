import os
from email.message import EmailMessage
import imghdr
import smtplib
import threading
import time

# gets the sender's address and password
address = os.environ.get('sender_mail')
password = os.environ.get('sender_pass')
# msg will have attributes added on it later on
msg = EmailMessage()


def create_email(recipient):
    """Adds the
    subject
    from, to, and body attributes to the email message"""
    
    msg['Subject'] = input("\nPlease type the subject of the email: ")
    msg['From'] = address
    msg['To'] = recipient
    body = input("\nPlease type the body of the email: ")

    msg.set_content(body)


def add_image():
    """Prompts the user to enter an image name and proceeds to append it to the existing email message
    Image data must be read in read-binary,
    The full image name is needed, such as image.jpg"""

    try:
        file_name = input("\nType the image's full name (ex. image.png, picture.jpg): ")
        with open(file_name, 'rb') as f:
            img_data = f.read()
            img_type = imghdr.what(f.name)
            img_name = f.name

            msg.add_attachment(img_data, maintype='image', subtype=img_type, filename=img_name)

    except FileNotFoundError:
        print("\nThe file you typed does not exist.")
        quit()


def send_email(spam=False, thread=None):
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
        server.set_debuglevel(1)
        server.starttls()
        server.ehlo()
        server.login(address, password)
        server.send_message(msg)

        if not spam:
            print("\nEmail has been sent.")
        if spam:
            print(f"Email {thread+1} has been sent.")

        server.quit()

    except smtplib.SMTPAuthenticationError:
        print("\nYou gave the incorrect login information for your gmail account.")
        quit()
    except smtplib.SMTPRecipientsRefused:
        print("\nThe email address which you wish to email does not exist.")
        quit()


def send_spam():
    """This function:
    prompts user for number of emails to be sent,
    creates as many Thread() instances as the user requested,
    starts each thread via for loop with half-second delay
    joins each thread via for loop,

    each thread executes send_mail(spam=True, thread=t)
    and is created via list comprehension"""

    num = int(input("\nType the number of emails the recipient will receive: "))

    threads = [threading.Thread(target=send_email, args=(True, t), daemon=True) for t in range(num)]

    for thread in threads:
        thread.start()
        # time.sleep(0.5)

    for thread in threads:
        thread.join()


def main():
    target = input("\nType the recipient's full gmail (ex. johndoe@gmail.com): ")
    create_email(target)

    is_attachment = input("\nWould you like to attach an image to the email? [y/n]: ")
    if is_attachment == "y":
        add_image()

    is_spam = input("\nWould you like to spam the recipient? [y/n]: ")
    if is_spam == "y":
        send_spam()
    else:
        send_email()


if __name__ == "__main__":
    main()
