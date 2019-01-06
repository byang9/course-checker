#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import random
import urllib.request as urllib
from bs4 import BeautifulSoup
import json
import smtplib
from email.mime.text import MIMEText

found = False
schoolUrls = {"GT":"https://oscar.gatech.edu/pls/bprod/bwckschd.p_disp_detail_sched?term_in=201902&crn_in="}

def reminder(body):
    cred = json.load(open('credentials.json'))  # Credentials
    if cred['gmail'] != '' and cred['gmailPass'] != '':
        msg = MIMEText(body)
        msg['Subject'] = 'CourseChecker - Course available'
        msg['From'] = 'CourseChecker@coursechecker.com'
        msg['To'] = cred['gmail']
        s = smtplib.SMTP('smtp.gmail.com',587)
        s.ehlo()
        s.starttls()
        s.login(cred['gmail'],cred['gmailPass'])
        s.sendmail(msg['From'], [cred['gmail']], msg.as_string())
        s.quit()

def fromGT(crn=''):
    global found
    site = schoolUrls["GT"] + crn
    page = urllib.urlopen(urllib.Request(site))
    soup = BeautifulSoup(page, 'html.parser', from_encoding='utf-8')

    # Finding number of slots open
    info = soup.findAll(attrs={"class":"dddefault"})
    openSlots = int(str(info[0]).split('<td class="dddefault">')[4].split('<')[0])

    if openSlots > 0 and not found:
        reminder('You have a slot available for CRN: {}!!!'.format(crn))
        found = True
    elif openSlots == 0:
        found = False

    return openSlots > 0


if __name__=='__main__':
    ping,maxPing,totalSeconds = 0,3,0

    while (ping < maxPing):
        m,s = divmod(totalSeconds,60)
        h,m = divmod(m,60)
        slot = fromGT('31562')
        print("[%d:%02d:%02d] {}".format("Slot open!!" if slot else "N/A") % (h, m, s))
        randSec = random.randint(4,7) # Randomly waits between 4 and 7 seconds
        time.sleep(randSec)
        ping +=1
        totalSeconds += randSec

