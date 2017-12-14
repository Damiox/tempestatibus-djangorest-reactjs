import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


# Service to send an e-mail w/ imageAttachment (optional)
class EmailService:
    # You need to configure the sender auth in sendmail
    SENDER = 'damiox@gmail.com'

    def send(self, receipt, subject, bodyPlain, bodyHtml, imageAttachment):
        # Create message container
        # The correct MIME type is multipart/alternative.
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = subject
        msgRoot['From'] = EmailService.SENDER
        msgRoot['To'] = receipt
        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide
        # which they want to display.
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        # Record the MIME types of both parts - text/plain and text/html.
        msgText1 = MIMEText(bodyPlain, 'plain')
        msgText2 = MIMEText(bodyHtml, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message,
        # in this case the HTML message, is best and preferred.
        msgAlternative.attach(msgText1)
        msgAlternative.attach(msgText2)

        # Adding Image
        if imageAttachment is not None:
            fp = open(imageAttachment, 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()
            msgImage.add_header('Content-ID', '<image>')
            msgRoot.attach(msgImage)

        # Send the message via local SMTP server.
        s = smtplib.SMTP('localhost')
        s.sendmail(EmailService.SENDER, receipt, msgRoot.as_string())
        s.quit()
