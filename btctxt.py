#!/usr/bin/python

#import libraries
import sys
import time
import ConfigParser
import urllib2
import smtplib
import getpass
from socket import gaierror
from socket import error as socketerror
from email.mime.text import MIMEText


class BTCtxtError(Exception):

    def __init__(self, message, cause):
        super(BTCtxtError, self).__init__(
            '{}, caused by {}'.format(message, repr(cause)))
        self.cause = cause


class ParserError(Exception):
    pass


class BTCtxt:

    def __init__(self):
        self.last = 1
        self.from_address = ""
        self.smtp = ""
        self.port = ""
        self.to_address = ""
        self.user = ""
        self.pw = ""
        self.ratio = []
        self.sleeptime = []
        self.currency = ""
        return None

    def monitor(self):
        api_url = "https://api.bitcoinaverage.com/ticker/global/"
        url = "{}{}/last".format(api_url, btctxt.currency)
        # get current price
        try:
            current = float(urllib2.urlopen(url).read())
        except(urllib2.HTTPError) as e:
            raise BTCtxtError("Invalid URL: {}".format(url), e)
        else:
            # compare current to log price
            change = abs((btctxt.last - current) / current)
            if change > btctxt.ratio:
                try:
                    btctxt.send_email(current)
                except smtplib.SMTPAuthenticationError as e:
                    raise BTCtxtError('Email log-in failed', e)
                except gaierror as e:
                    raise BTCtxtError(
                        'Invalid server {}'.format(self.smtp), e)
                except socketerror as e:
                    msg = "Invalid (server, port): "
                    raise BTCtxtError('{}({}, {})'.format(msg, self.smtp,
                                                          self.port), e)
            else:
                btctxt.last = current
        return self

    def send_email(self, current):
        msg = self._write_email(current)
        # start server
        try:
            server = smtplib.SMTP(self.smtp, self.port, None, 30)
            server.ehlo()
            server.starttls()
            server.login(self.user, self.pw)
            server.sendmail(self.from_address, [self.to_address],
                            msg.as_string())
        finally:
            server.close()

    def _write_email(self, current):
        # Format email_content
        timestr = time.strftime("%H:%M", time.localtime())
        email_content = ("{}/BTC: {} as of {}.").format(self.currency,
                                                        current,
                                                        timestr)
        # Create msg
        msg = MIMEText(email_content)
        msg['Subject'] = "BTCtxt"
        msg['To'] = self.to_address
        msg['From'] = self.from_address
        return msg


def get_conf(path):
    parser = ConfigParser.RawConfigParser()
    parser.read(path)
    necessary = ["smtp", "port", "to", "from"]
    optional = ["currency", "sleeptime", "ratio"]
    # check necessary
    for item in necessary:
        if item not in parser.options("Necessary"):
            raise ParserError(
                "Please include a {} entry within [Necessary].".format(item))
    # check optional
    for item in optional:
        if item not in parser.options("Optional"):
            if item is "currency":
                parser.set("Optional", item, "USD")
            elif item is "sleeptime":
                parser.set("Optional", item, "180")
            elif item is "ratio":
                parser.set("Optional", item, "0.075")
    return parser


if __name__ == '__main__':
    # Create instance of btctxt class
    btctxt = BTCtxt()
    # Populate btctxt attributes using one of three input methods
    if len(sys.argv) >= 2:
        #read .conf
        parser = get_conf(sys.argv[1])
        # write .conf to btctxt
        btctxt.from_address = parser.get("Necessary", "from")
        btctxt.smtp = parser.get("Necessary", "smtp")
        btctxt.port = parser.get("Necessary", "port")
        btctxt.to_address = parser.get("Necessary", "to")
        btctxt.ratio = float(parser.get("Optional", "ratio"))
        btctxt.sleep_time = float(parser.get("Optional", "sleeptime"))
        btctxt.currency = parser.get("Optional", "currency")
        if len(sys.argv) == 2:
            # if only path to .conf file provided
            # get user and pw from std in
            btctxt.user = raw_input("Username: ")
            btctxt.pw = getpass.getpass()
        elif len(sys.argv) == 3 and sys.argv[2] is "c":
            # if path to .conf file and letter c provided as second argument
            btctxt.user = parser.get("Credentials", "user")
            btctxt.pw = parser.get("Credentials", "pw")
    else:
        # read stdin
        btctxt.from_address = sys.argv[1]
        btctxt.smtp = sys.argv[2]
        btctxt.port = sys.argv[3]
        btctxt.to_address = sys.argv[4]
        btctxt.user = sys.argv[5]
        btctxt.pw = sys.argv[6]
        btctxt.ratio = float(sys.argv[7])
        btctxt.sleep_time = float(sys.argv[8])
        btctxt.currency = sys.argv[9]
    while True:
        btctxt = btctxt.monitor()
        time.sleep(btctxt.sleep_time)
