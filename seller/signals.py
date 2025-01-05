import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SellerInformation, S_User
from home.models import User
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def email_sender(To, subject, message):
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_From = 'jemsmpatel1310@gmail.com'
    EMAIL_HOST_PASSWORD = 'atslgccdcjdlswba'
    msg = MIMEMultipart()
    msg['From'] = EMAIL_From
    msg['To'] = To
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    try:
        smtp = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_From, EMAIL_HOST_PASSWORD)
        smtp.sendmail(EMAIL_From, To, msg.as_string())
        logger.info("Email sent successfully to %s", To)
    except smtplib.SMTPException as e:
        logger.error("Failed to send email: %s", e)
    finally:
        smtp.quit()
        logger.info("[*] Connection closed")




@receiver(post_save, sender=User)
def send_email_on_user_save(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to ShopingMart Platform'
        message = f'''\nHi {instance.email},\nthank you for registering at our site.\nYour seller ID is created successfully: \n\nThanks and visit again.'''
        email_sender(instance.email, subject, message)
        logger.info("Email sent on user creation for %s", instance.email)






@receiver(post_save, sender=S_User)
def send_email_on_user_save(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to ShopingMart Platform'
        message = f'''\nHi {instance.Email},\nthank you for registering at our site.\nYour seller ID is created successfully: {instance.Seller_Id}\n\nThanks and visit again.'''
        email_sender(instance.Email, subject, message)
        logger.info("Email sent on user creation for %s", instance.Email)

@receiver(post_save, sender=SellerInformation)
def send_email_on_seller_info_save(sender, instance, created, **kwargs):
    try:
        ema = S_User.objects.get(Seller_Id=instance.Seller_Id)
    except S_User.DoesNotExist:
        logger.error("No S_User found with Seller_Id %s", instance.Seller_Id)
        return

    if created:
        subject = 'Welcome to ShopingMart Platform'
        message = f'''\nHi {ema.Email},\nthank you for registering at our site.\n\nThanks and visit again.'''
        email_sender(ema.Email, subject, message)
        logger.info("Email sent on seller information creation for %s", ema.Email)
    elif instance.status == "valid":
        subject = 'Validation Successful For Seller Registration'
        message = f'\nHi {ema.Email}, \nYour data has been validated successfully.\nThanks for joining our site.\nVisit again.'
        email_sender(ema.Email, subject, message)
        logger.info("Email sent on validation success for %s", ema.Email)
    elif instance.status == "invalid":
        subject = 'Validation Unsuccessful For Seller Registration'
        message = f'\nHi {ema.Email},\nYour data has not been validated successfully.\nPlease try again.\nIf you have any problems, contact us at {"http://192.168.201.181:8000/contact"}.\nThank you for joining ShopingMart Platform.'
        email_sender(ema.Email, subject, message)
        logger.info("Email sent on validation failure for %s", ema.Email)
