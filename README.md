This python script may be used to monitor the price of bitcoin and send email alerts when the price has changed significantly.

To use it, modify the bash file example-btctxt and replace the arguments with your appropriate values.

The default file is:

#!/bin/bash
~/bin/btctxt/btctxt.py ~/bin/price username@gmail.com username password smtp.gmail.com 587 5551234567@vtext.com .1 180

Step 0: Point the bash file to your btctxt.py. Currently, it's pointing to the user's home directory bin.
	
Step 1: Set the first argument, "path", to the path to you'd like to keep your price log. The price log is a file that simply contains the last price that was notified to the user. In the example, this file is stored at ~/bin/price.

Step 2: Set the second argument, "from_address". This is simply your email address.

Step 3: Set the third argument, "user". This is the username portion of your email server's login credentials. In the example script, the username is creatively named "username".

Step 4: Set the fourth argument, "pw". Similar to (Step 3), this is the password portion of your email server's login credentials.

Step 5: Set the fifth argument, "SMTP". This is the SMTP address of your email server. For gmail, it is smtp.gmail.com

Step 6: Set the sixth argument, "port". This is the port of your email server. For gmail, it is port 587.

Step 7: Set the seventh argument, "to_address". This is your the email address that corresponds to your cell providers sms server. For verizon it [9digitnumber]@vtext.com

Step 8: Set the eighth argument, "ratio". This is the proportional change in price at which btctxt should send you an email. In the example, we would want to be notified at a 10% change in price.

Step 9: Set the nineth argument, "sleepTime". This is the amount of time (in seconds) btctxt should wait between checking the price of btc. In the example, btctxt waits 180 seconds between checking the price.

