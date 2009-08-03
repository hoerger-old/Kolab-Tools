"""
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <hanse@otrn.org> wrote this file. As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return.
 *	 Hans-Jörg Schurr
 * ----------------------------------------------------------------------------
"""

server = "mailbox.4-mail.net"
user="hanse@otrn.org"
password="asdf"
calendarfolder="INBOX/Birthday_Calendar"
icalurl="http://example.com"

import urllib2, uuid, datetime
import imaplib, email
from email.message import Message
from email.generator import Generator
from cStringIO import StringIO
from icalendar import Calendar, Event, vDatetime
from xml.etree import cElementTree as ElementTree
from xml.etree.cElementTree import Element

class event:
	def __init__(self, uuid=uuid.uuid1(), start_date=None, end_date=None, creation_date=datetime.datetime.now(), summary="", location="", recurrence=None):
		self.uuid = uuid
		self.start_date = start_date
		self.end_date = end_date
		self.creation_date = creation_date
		self.summary = summary
		self.location = location
		self.recurrence = None # currently incomplete 
	def from_xml(self, xml):
		# only summary and uuid is currently relevant
		etree = ElementTree.fromstring(xml)
		self.uuid = etree.find("uid").text
		self.summary = etree.find("summary").text
	def from_ical(self, ical):
		self.uuid = uuid.uuid1()
		self.start_date = ical.decoded('dtstart')
		self.end_date = ical.decoded('dtstart')
		self.summary= ical.decoded('summary')
		self.recurrence = ical.decoded('rrule')['FREQ'][0]
	def to_xml(self):
		event = Element("event")
		event.set("version","1.0")
		
		uid = Element("uid")
		uid.text=self.uuid.hex
		event.append(uid)
		summary = Element("summary")
		summary.text=self.summary
		event.append(summary)
		location = Element("location")
		location.text=self.location
		event.append(location)		
		start_date = Element("start-date")
		start_date.text=self.start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
		event.append(start_date)	
		end_date = Element("end-date")
		end_date.text=self.end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
		event.append(end_date)	
		creation_date = Element("creation-date")
		creation_date.text=self.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ")
		event.append(creation_date)	
		
		if self.recurrence:
			rec = Element("recurrence")
			rec.set("cycle",self.recurrence.lower())
			rec.set("type", "daynumber")
			interval = Element("interval")
			interval.text = "1"
			rec.append(interval)
			event.append(rec)
	
		io = StringIO()
		tree = ElementTree.ElementTree(event)
		tree.write(io)
		return '<?xml version="1.0"?>'+io.getvalue()
	def to_ical(self):
		pass

def get_event_object(msg):
	for part in msg:
		if isinstance(part, tuple):
			mail = email.message_from_string(part[1])
			for msg_part in mail.walk():
				if msg_part.get_content_type()=="application/x-vnd.kolab.event":
					#got kolab event object
					e = event()
					e.from_xml(msg_part.get_payload(decode=True))
					return e

def fetch_calendar(mailbox):
	l = []
	for e in mailbox.search(None, 'ALL')[1][0].split():
		obj = get_event_object(M.fetch(e,'(RFC822)')[1])
		if obj:
			l.append(obj)
	return l

def sync(mailbox, icalendar):
	def find(f, i):
		for o in i:
			if f(o):
				return o

	kolab_calendar = fetch_calendar(mailbox)
	for ievent in icalendar.walk('vevent'):
		nevent = event()
		nevent.from_ical(ievent)
		if not find(lambda x: nevent.summary == x.summary, kolab_calendar):
			from email.mime.multipart import MIMEMultipart
			from email.mime.application import MIMEApplication

			kolab_email = MIMEMultipart()
			kolab_email["Subject"] = nevent.uuid.hex
			kolab_email["X-Kolab-Type"] = "application/x-vnd.kolab.event"
        
			kolab_attachment = MIMEApplication(nevent.to_xml(), "x-vnd.kolab.event", email.encoders.encode_quopri)
			kolab_attachment["Content-Disposition"]= "attachment"
			kolab_email.attach(kolab_attachment)
			mailbox.append(calendarfolder, None, None, kolab_email.as_string())
			

if __name__=="__main__":
	icalendar = urllib2.urlopen(icalurl)

	print "Reading iCalendar"
	cal = Calendar.from_string(icalendar.read())
	icalendar.close()

	print "Connecting to IMAP server"
	M = imaplib.IMAP4(server)
	print "Login as", user
	M.login(user, password)

	M.select(calendarfolder)

	print "Syncronizing..."
	sync(M, cal)
	#for c in fetch_calendar(M):
	#	print c.uuid ,c.summary
			
	print "Logout"
	M.logout()
