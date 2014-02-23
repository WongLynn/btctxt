#BTCtxt

BTCtxt monitors the price of BTC by grabbing the current price from bitcoinaverage.com and sending an email alert when the price has changed significantly. Since cellphones have a corresponding email address, BTCtxt can submit an smtp message as an sms message to your phone.

#Calling BTCtxt

##(Option 1) Fully from command line arguments

###Example: 


>    $ btctxt.py username@gmail.com smtp.server.com port 5551234567@cell.com user pw .1 180 USD

###Arguments
1. Provide a path to a valid directory in which you'd like to store a blank file. If a file does not exist, BTCtxt will create a fill with value 1. This guarantees you'll receive a txt the first time BTCtxt successfully runs.
2. The email address from which you'd like to send the sms message.
3. Your SMTP server. For gmail, it's smtp.gmail.com
4. Your SMTP server's port. For gmail, it's port 587.
5. The email address you wish to send your alert to. For verizon it is [9digitnumber]@vtext.com
6. Your email username.
7. Your email password.
8. The proportional change in price you'd wish to be notified at. 0.1 implies BTCtxt will view a 10% change in price as an alert worthy event.
9. The amount of time (in seconds) BTCtxt should wait between checking the price. 180 implies 180 seconds between checks.
10. The currency you wish to monitor.
    
    This value will be substituted into the string concatanation:
    
    "https://api.bitcoinaverage.com/ticker/global/" + currency + "/last"
    
     So, be sure to verify you are producing a valid URL by visiting the site beforehand.

##(Option 2) Partly from .conf file/ partly from command line arguments

###Example:

>    $ btctxt.py ./btctxt.conf
>
>    Username: myUsername
>
>    Password: _

This option is intended to be a compromise of convenience and security (i.e., not leaving a .conf file or bash script lying around with your email credentials in it).

###Arguments
1. Path to your .conf file. See example.conf for details 
2. Enter your email username (received as python raw_input())
3. Enter your email password (received as python getpass.getpass())

The rest of the information will either be drawn from your .conf file or be set to default values if no value is provided.

##(Option 3) Fully from .conf file

###Example:

>
>    $ btctxt.py ./btctxt.conf c

###Arguments
1. Path to your .config file. See example.conf for details
2. The letter c, for credentials I suppose.

This option assumes you've added something like the following 
section to your .conf file.

> [Credentials]
>
> user = myUsername
>
> pw = myPassword

Just to be clear here: if you decide to go with option 3, 
you're deciding to keep your credentials in plain text
on your pc at your own risk.
