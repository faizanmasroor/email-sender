# :mailbox: SMTP Gmail Script :mailbox:

#### A Python script that can automate sending emails, featuring dynamically entered attributes (email recipient, subject line, email body) and image attachments.

## Installation and Usage

#### 1. [Clone](https://docs.github.com/articles/cloning-a-repository) the repository
```powershell
git clone https://github.com/faizanmasroor/email-sender.git
```
#### 2. Turn on [2-Step Verification](https://myaccount.google.com/signinoptions/twosv) for the Google account you will be using to send emails
#### 3. Generate an [app password](https://myaccount.google.com/apppasswords) for your Google account
#### 4. Type "Edit environment variables for your account" in the Windows search bar and open the Environment Variables window
#### 5. Create the "SENDER_MAIL" and "SENDER_PASS" user variables as shown
![image](https://github.com/faizanmasroor/email-sender/assets/107204129/4890c7f7-b9ec-4e83-982e-967e104eea64)
#### 6. Open your CLI and use Python to [run](https://docs.python.org/3/using/cmdline.html) the script within the repository; answer the prompts that follow
```powershell
python email-sender/email_sender.py
```

## Required Dependencies

* Python <3.13[^1]

## Video Demo
https://github.com/faizanmasroor/email-sender/assets/107204129/0ac50533-24b1-4431-823e-ba2508ec7e5b

## Goal
<b> To create and send an email with customizable input—including recipient email, subject line, email body, and image attachments—from a Gmail account, whose username and password are declared as environment variables </b>

## Methodology

* Get the username and password of the user's email (which is used to send emails) from environment variables
* Generate an EmailMessage object (from email.message) to craft an email and append features
* Prompt the user for the email's recipient, subject, and body
* Prompt the user for however many images they wish to attach to their email
  * Use the built-in add_attachment method in EmailMessage to attach the image to the email
* Send the email via SMTP (port 587)
  * Establish a connection to Gmail's SMTP server
  * Enable the TLS protocol
  * Log into the user's Gmail account
  * Send an email message to the server
  * Close connection

[^1]: The module imghdr (a library used in the script) will be supported with Python ≥3.13; aside from this, there are no other dependency constraints.
