#!/usr/bin/python

#import libraries
import sys
import os
import urllib2
from BeautifulSoup import BeautifulSoup
import time
from email.mime.text import MIMEText
import smtplib

#read stdin
path = sys.argv[1]
from_address = sys.argv[2]
user = sys.argv[3]
pw = sys.argv[4]
smtp = sys.argv[5]
port = sys.argv[6]
to_address = sys.argv[7]
ratio = float(sys.argv[8])
sleepTime = float(sys.argv[9])


def main(path, from_address, user, pw, smtp, port, to_address, ratio):
        #get current price
        web = urllib2.urlopen("http://bitcoinity.org/markets/bitstamp/USD").read()
        soup = BeautifulSoup(''.join(web))
        last = float(soup.find('span', id="last_sell").string)
        #check last price
        checkLogExistence(path)
        logP = getLog(path)
        change = abs((logP-last)/last)
        if change > ratio:
                notify(last, path, from_address, user, pw, smtp, port, to_address)
        return None


def notify(last, path, from_address, user, pw, smtp, port, to_address):
        sendEmail(last, from_address, user, pw, smtp, port, to_address)
        writeLog(last, path)
        return None


def sendEmail(last, from_address, user, pw, smtp, port, to_address):
        #Format email_content
        timestr = time.strftime("%H:%M", time.localtime())
        email_content = "The price of BTC is currently " + str(last) + " as of " + timestr
        #Create msg
        msg = MIMEText(email_content)
        msg['Subject'] = "BTC-Update"
        msg['To'] = to_address
        msg['From'] = from_address
        #start server
        server = smtplib.SMTP(smtp + ":" + port)
        server.ehlo()
        server.starttls()
        #login
        server.login(user, pw)
        #send msg
        server.sendmail(from_address, [to_address], msg.as_string())
        server.quit
        return None


def writeLog(last, path):
        f = open(path, 'w')
        f.write(str(last))
        f.close()
        return None


def getLog(path):
        f = open(path, 'r')
        price = float(f.read())
        f.close()
        return price


def checkLogExistence(path):
        if not os.path.exists(path):
                f = file(path, 'w')
                f.write("1")
                f.close()
        return None


while True:
        main(path, from_address, user, pw, smtp, port, to_address, ratio)
        sleep(sleepTime)
