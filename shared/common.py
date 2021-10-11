"""
    File name: common.py
    Added by: FR7 ~ Farah Elkourdi 
    Date created: 10/08/2021
    Date last modified: 10/08/2021
    Description: includes functions that could be common in APIs or can be reused in other projects. 
"""
import re
import random 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP

def send_email(user_email, msg):
    """
    Send email
    """
    sender_email = "ssw555.halcyon@gmail.com"
    password = "SSW555team1"
    receiver_email = user_email
    message = MIMEMultipart("alternative")
    message["Subject"] = "Account activation"
    message["From"] = sender_email
    message["To"] = receiver_email
    message.attach(MIMEText(msg, "html"))
    msgBody = message.as_string()
    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msgBody)

def generate_code():
    """ 
    generate code 
    """
    code = ''.join(random.sample('123456789', 5))
    return code

def check_password (user_pass):
    """
    Check sign up password 
    """
    if (len(user_pass)<8):
        flag = False
    elif not re.search("[a-z]", user_pass):
        flag = False
    elif not re.search("[A-Z]", user_pass):
        flag = False
    elif not re.search("[0-9]", user_pass):
        flag = False
    else:
        flag = True          
    return flag


def is_dirty(myobj):
    """
    check if any value in object is changed from its previous values
    """
    from sqlalchemy.orm import class_mapper
    from sqlalchemy import inspect
    inspr = inspect(myobj)
    attrs = class_mapper(myobj.__class__).column_attrs  # exclude relationships
    for attr in attrs:
        hist = getattr(inspr.attrs, attr.key).history
        if hist.has_changes():
            return True
    return False
