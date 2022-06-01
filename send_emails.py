"""
Script to identify the next email in sequence based on date and send it to myself
Set this up on a cron trigger every weekday
"""

import datetime 
import glob

import smtplib, ssl
import email.message 
from decouple import config

port = 465  # For SSL
user = config("sender_email")
password = config("password")
target = config("receiver_email")
path_offset = config("root_path")


def get_next_subject_and_body(path_offset): 
    """ 
    Get the next file in sequence, return its text as subject + parsed file name as body
    """

    print("starting job for ", datetime.datetime.today())
    files = glob.glob(path_offset+'email_text/*.txt')
    files.sort()
    
    index = get_index_from_length(len(files))
    f = files[index]

    subject = '[tickler_links] ' + f.split('/')[-1].split('_')[-1].split('.')[0]
    body = open(f).read()
    return subject, body


def get_index_from_length(l):
    """ 
    Get the next index every weekday within a range l, looping back to beginning at day l+1
    """

    today = datetime.datetime.today()-datetime.timedelta(hours=6) # get into roughly UTC
    today = datetime.date(today.year, today.month, today.day) 
    
    base_week = datetime.date(2022, 3, 7) # arbitrary start date 
    weeks_elapsed = (today - base_week).days//7
    weekdays_elapsed = today.weekday() # indexes to 0 = monday

    index = (weeks_elapsed*5 + weekdays_elapsed + 2) # add offset bc didn't like how original days of week were lining up

    return(index%l)


def send_email(subject, body, test=False): 
    """ 
    Send email with subject, body and sender/recipient from config

    if 'test': bypass sending email and just print the body (for developing)
    """

    sender_email = user
    receiver_email = "kevin@mojo.com"

    msg = email.message.Message()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.add_header('Content-Type', 'text')
    msg.set_payload(body)
    msg.set_charset('utf-8')
    
    # Create a secure SSL context
    context = ssl.create_default_context() # validate certificate

    if test:
        print(msg.as_string())
        return 

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server: # close connection after block
        server.login(user, password)
        
        # send email
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        print("email sent: ", subject)


def main(): 
    
    subject, body = get_next_subject_and_body(path_offset=path_offset)
        # path_offset from root to this directory to run from cron
    
    send_email(subject, body, test=False)
    
    # for local testing:
    # subject, body = get_next_subject_and_body(path_offset='')
    # send_email(subject, body, test=True)

main()