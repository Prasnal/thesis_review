import requests
from bs4 import BeautifulSoup
import config as cfg
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib
import schedule
import time

def send_email(reviews):
    gmail_user = cfg.email['username']
    gmail_password = cfg.email['password']
    email=cfg.email_to

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = email
    msg['Subject'] = 'You have a new review!'

    body = 'You got the review from: {}'.format(reviews)
    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_user, gmail_password)
    server.sendmail(gmail_user, email, text)
    server.quit()

def get_review():

    url = 'https://misio.ftj.agh.edu.pl/opm/acceptedlist/?name=2017/18'                                
    msc_list=requests.post(url, verify=False)

    soup = BeautifulSoup(msc_list.text, 'html.parser')
    result = [i.find_all('td') for i in soup.find_all('tr') if cfg.personal_data in str(i)][0]
    reviews = [i.text for i in result[3].find_all() if 'Recenzja' in str(i)]

    if len(reviews)>cfg.reviews_number:
        send_email(reviews)


schedule.every(1).minutes.do(get_review)
while True:
    schedule.run_pending()
    time.sleep(1)

