from flask_mail import Mail, Message

mail = Mail()


def send_email(subject, sender, recipients, html):

    # received maybe too many
    msg = Message(
        subject=subject,
        sender=sender,
        recipients = [recipients]
    )

    msg.html = html

    msg.send()