# -*- coding: utf-8 -*-

import smtplib
import csv
from email.mime.text import MIMEText
from email.Header import Header
from email.Utils import formatdate

from_addr  = ''
username = from_addr
password = ''
sbj = ''
i = 1

f = open( '/tex.txt', 'r' )
tex = f.read()
f.close

#### Edit Message using smtplib
def EditMessage( x, y ):
    #print 'ng'
    msg = MIMEText( x, 'plain', 'utf-8' )
    msg['Subject'] = Header( sbj, 'utf-8' )
    msg['From'] = from_addr
    msg['To'] = y
    msg['Date'] = formatdate()

    s = smtplib.SMTP( '' )
    s.starttls()
    s.login( username, password )
    s.ehlo()
    s.sendmail( msg['From'], msg['To'], msg.as_string() )
    s.quit()

#### Get and edit csv
with open( 'test.csv', 'r' ) as f:
    info_reader = csv.reader(f)
    for row in info_reader:
        first_line = row[0] + ' ' + ''
        ## Replace mail's apostrophe
        to_addr = row[1].replace( '\'', '' )
        body = first_line + '\n' + '\n' + tex
        EditMessage( body, to_addr )
        #print row[0]
        #print row[1]
        print i
        i += 1

f.close()
