#!/usr/bin/python

#import libraries
import sys
import os
import time
import ConfigParser
import urllib2
import smtplib
import getpass
from email.mime.text import MIMEText


class BTCtxt:
        def __init__(self):
                self.last=1
                self.from_address=""
                self.smtp=""
                self.port=""
                self.to_address=""
                self.user=""
                self.pw=""
                self.ratio=[]
                self.sleeptime=[]
                self.currency=""
                return None


        def monitor(self):
                #get current price
                current = float(urllib2.urlopen("https://api.bitcoinaverage.com/ticker/global/" + btctxt.currency + "/last").read())
                #compare current to log price
                change = abs((btctxt.last-current)/current)
                if change > btctxt.ratio:
                        btctxt.sendEmail(current)
                        btctxt.last=current
                return self


        def sendEmail(self, current):
                #Format email_content
                timestr = time.strftime("%H:%M", time.localtime())
                email_content = "The price of BTC is currently " + str(current) + self.currency + " as of " + timestr + "."
                #Create msg
                msg = MIMEText(email_content)
                msg['Subject'] = "BTCtxt"
                msg['To'] = self.to_address
                msg['From'] = self.from_address
                #start server
                server = smtplib.SMTP(self.smtp + ":" + self.port)
                server.ehlo()
                server.starttls()
                #login
                server.login(self.user, self.pw)
                #send msg
                server.sendmail(self.from_address, [self.to_address], msg.as_string())
                server.quit()
                return None


def getConf(path):
        parser = ConfigParser.RawConfigParser()
        parser.read(path)
        necessary = ["smtp", "port", "to", "from"]
        optional = ["currency", "sleeptime", "ratio"]
        #check necessary
        for item in necessary:
                if item not in parser.options("Necessary"):
                        print "Please include a " + item + " entry in the [Necessary] section."
                        return False
        #check optional
        for item in optional:
                if item is "currency":
                        parser.set("Optional", item, "USD")
                elif item is "sleeptime":
                        parser.set("Optional", item, "180")
                elif item is "ratio":
                        parser.set("Optional", item, "0.075")          
        return parser


if __name__ == '__main__':
        #Create instance of btctxt class
        btctxt=BTCtxt()
        #Populate btctxt attributes using one of three input methods
        if len(sys.argv) == 2: #if only path to .conf file provided 
                #read .conf
                parser = getConf(sys.argv[1])
                #write .conf to btctxt
                btctxt.from_address = parser.get("Necessary", "from")
                btctxt.smtp = parser.get("Necessary", "smtp")
                btctxt.port = parser.get("Necessary", "port")
                btctxt.to_address = parser.get("Necessary", "to")
                btctxt.ratio = float(parser.get("Optional", "ratio"))
                btctxt.sleepTime = float(parser.get("Optional", "sleeptime"))
                btctxt.currency = parser.get("Optional", "currency")
                #get user and pw from std in
                btctxt.user = raw_input("Username: ")
                btctxt.pw = getpass.getpass()
        elif len(sys.argv) == 3 and sys.argv[2] is "c": #if path to .conf file and letter c provided as second argument
                #read .conf
                parser = getConf(sys.argv[1])
                #write .conf to btctxt
                btctxt.from_address = parser.get("Necessary", "from")
                btctxt.smtp = parser.get("Necessary", "smtp")
                btctxt.port = parser.get("Necessary", "port")
                btctxt.to_address = parser.get("Necessary", "to")
                btctxt.ratio = float(parser.get("Optional", "ratio"))
                btctxt.sleepTime = float(parser.get("Optional", "sleeptime"))
                btctxt.currency = parser.get("Optional", "currency")
                btctxt.user = parser.get("Credentials", "user")
                btctxt.pw = parser.get("Credentials", "pw")
        else:
                #read stdin
                btctxt.from_address = sys.argv[1]
                btctxt.smtp = sys.argv[2]
                btctxt.port = sys.argv[3]
                btctxt.to_address = sys.argv[4]
                btctxt.user = sys.argv[5]
                btctxt.pw = sys.argv[6]
                btctxt.ratio = float(sys.argv[7])
                btctxt.sleepTime = float(sys.argv[8])
                btctxt.currency = sys.argv[9]
        while True:
                btctxt.monitor()
                time.sleep(btctxt.sleepTime)
