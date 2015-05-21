#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys,os,re,sys
import smtplib
import requests

def register():

	CON = lite.connect('db-nfc.db')

	ATQA = 0
	UID = 0
	SAK = 0
	CLIST = []
	CDATA = 0
	NAME = ''
	SURNAME = ''
	PHONE = 0
	MAIL = ''

	try:
		while(True):

			print 'Yeni Kart Girisi..'
			nfc_data = os.popen('sudo /home/pi//libnfc-1.7.1/examples/./nfc-poll').readlines()
			os.popen('sudo /home/pi/wiringPi/examples./softTone')

			for i in range(1,len(nfc_data)):
				search = re.search(r'\):(.*)',nfc_data[i], re.M|re.I)
				if search is None:
					CDATA = 0
				else:
					CDATA = search.group(1).replace(" ","")

				CLIST.append(CDATA)

			ATQA = CLIST[0]
			UID  = int(CLIST[1],16)
			SAK  = CLIST[2]

			NAME = raw_input('Isim: ')
			SURNAME = raw_input('Soyisim: ')
			PHONE = int(raw_input('Telefon: '))
			MAIL = raw_input('Mail:')

			with CON:

				cur = CON.cursor()
				cur.execute("INSERT INTO users(ATQA,UID,SAK,NAME,SURNAME,PHONE,MAIL) VALUES(?,?,?,?,?,?,?)",(ATQA,UID,SAK,NAME,SURNAME,PHONE,MAIL))

				'''
				cur.execute('SELECT * FROM users')
				data = cur.fetchall()
				for row in data:
					print row
				'''

				ATQA = 0
				UID = 0
				SAK = 0
				del CLIST[:]

				print 'Kayit Basarili.'
	except:
		print 'ERROR!'

	finally:
		if CON:
			CON.close()



def check_point():

    fromaddr = "oguzhancmd@gmail.com"
    msg = '\r\n'.join([
    'Subject: CheckSys Inc. ',
    '',
    'IP: NFC Test'])
    server  = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('oguzhancmd@gmail.com','rax30017080')
    text = msg




    CON = lite.connect('db-nfc.db')
    ATQA = 0
    UID = 0
    SAK = 0
    CLIST = []
    CDATA = 0

    while(True):

        print 'Lutfen Kartinizi Okutun..'
        nfc_data = os.popen('sudo /home/pi//libnfc-1.7.1/examples/./nfc-poll').readlines()
        for i in range(1,len(nfc_data)):
            search = re.search(r'\):(.*)',nfc_data[i], re.M|re.I)
            if search is None:
                CDATA = 0
            else:
                CDATA = search.group(1).replace(" ","")
                CLIST.append(CDATA)

		ATQA = CLIST[0]
        UID  = int(CLIST[1],16)
        SAK  = CLIST[2]
        

        with CON:
          cur = CON.cursor()
          cur.execute('SELECT NAME,SURNAME,MAIL FROM users WHERE UID =%s'%UID)
          data = cur.fetchone()

        if data is not None:
            os.popen('sudo /home/pi/wiringPi/examples/./softTone')
            print 'OK! - '+data[0]+' '+data[1]
            server.sendmail(fromaddr, data[2], text)
        else:
            print 'Kayit Bulunamadi'
            os.popen('sudo /home/pi/wiringPi/examples/./softTone')

        ATQA = 0
        UID = 0
        SAK = 0
        del CLIST[:]

def main():
    if(sys.argv[1]=='register'):
        register()
    if(sys.argv[1]=='help'):
        usage()
    if(sys.argv[1]=='check'):
        check_point()
    else:
        print 'finwe help'




if __name__ == '__main__':
    main()
