BTCtxt                        
===================================================== 

BTCtxt monitors the price of BTC by grabbing the current price from bitcoinity and sending an email alert when the price has changed significantly. Since cellphones have a corresponding email address, BTCtxt can submit an smtp message as an sms message to your phone.

Dependencies                     
======================================================

The only nonstandard library used in this application is the BeautifulSoup module. In the next release, I'm going to try to remove this dependency so that the entirity of this code is either a standard library or easily readable code. 


Calling BTCtxt                    
======================================================

(Option 1) Fully from the commandline
-----------------------------------------------------
>Example: 
>    $ btctxt.py ~/path/to/price username@gmail.com user pw smtp.server.com port 5551234567@cell.com .1 180

###Arguments
1. Provide a path to a valid directory in which you'd like to store a blank file. If a file does not exist, BTCtxt will create a fill with value 1. This guarantees you'll receive a txt the first time BTCtxt successfully runs.
2. The email address from which you'd like to send the sms message.
3. Your email username.
4. Your email password.
5. Your SMTP server. For gmail, it's smtp.gmail.com
6. Your SMTP server's port. For gmail, it's port 587.
7. The email address you wish to send your alert to. For verizon it is [9digitnumber]@vtext.com
8. The proportional change in price you'd wish to be notified at. 0.1 implies BTCtxt will view a 10% change in price as an alert worthy event.
9. The amount of time (in seconds) BTCtxt should wait between checking the price. 180 implies 180 seconds between checks.
10. The exchange you want to monitor (See 11 for example).
11. The currency you want to monitor.
    
    These values will be substituted into the string concatanation:
    
    "http://bitcoinity.org/markets/" + exchange + "/" + currency.
    
     So, be sure to verify you are producing a valid URL using your provided arguments by visiting bitcoinity beforehand.
    
12. Choose whether you wanted to monitor the last bid price (by providing "buy" as your argument) or the last ask price (by providing "sell" as your argument).

(Option 2) Partly from a config file/ partly from commandline
-------------------------------------------------------------
> Example:
>    $ btctxt.py ./btctxt.conf
>    Username: myUsername
>    Password: 

This option is intended to be a compromise of convenience and security (i.e., not leaving a .conf file or bash script lying around with your email credentials in it).

###Arguments
1. Path to your .config file. See example.conf for details 
2. Enter your email username (as python raw_input()
3. Enter your email password (as python getpass())

The rest of the information will either be drawn from your .conf file or be set to default values if no other value is provided.

(Option 3) Fully from a config file
--------------------------------------------------------------
> Example:
>    $ btctxt.py ./btctxt.conf c

###Arguments
1. Path to your .config file. See example.conf for details
2. The letter c, for credentials I suppose.

This option assumes you've added something like the following 
section to your .conf file.

> [Credentials]
> user = myUsername
>
> pw = myPassword

Just to be clear here: if you decide to go with option 3, 
you're deciding to keep your credentials in plain text
on your pc at your own risk.






