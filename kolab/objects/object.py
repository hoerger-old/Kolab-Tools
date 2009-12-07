# -*- coding: utf-8 -*-

import datetime
from xml.etree import cElementTree as ElementTree
from xml.etree.cElementTree import Element

class KolabObjectFormatError(Exception):
    def __init__(self, value, objectype):
        self.value = value
        self.objecttype=objecttype
    def __str__(self):
        return "Error in "+repr(self.objecttype)+": "+repr(self.value)

class KolabString(str):
    def __init__(self, *arg):
        str.__init__(self, *arg)
    
    @staticmethod
    def fromKolab(data):
        return KolabString(str(data))
    
    def toKolab(self):
        return str(self)
        

class KolabNumber(int):
    def __init__(self, *arg):
        int.__init__(self, *arg)

    @staticmethod
    def fromKolab(data):
        return KolabNumber(int(data))

    def toKolab(self):
        return str(self)


class KolabDate(datetime.date):
    def __init__(self, *arg):
        datetime.date.__init__(self, *arg)

    @staticmethod
    def fromKolab(data):
        return KolabDate(*datetime.datetime.strptime(data,"%Y-%m-%d").timetuple()[:3])

    def toKolab(self):
        return str(self.isoformat())

class KolabDateTime(datetime.datetime):
    def __init__(self, *arg):
        datetime.datetime.__init__(self, *arg)

	@staticmethod
	def fromKolab(data):
		return KolabDateTime(datetime.datetime.strptime(data, "%Y-%m-%dT%H:%M:%SZ"))

	def toKolab(self):
		return self.strftime("%Y-%m-%dT%H:%M:%SZ")

#helper functions for fields of type "date or datetime"
def DateOrDateTime(data):
    if len(data)>10:
        return KolabDate.fromKolab(data)
    else
        return KolabDateTime.fromKolab(data)

""" #RRGGBB """
class KolabColor:
	def __init__(self, colorString):
		r, g, b = colorString[1:3], colorString[3:5], colorString[5:] 
		self.r, self.g, self.b = [int(n, 16) for n in (r, g ,b)]

	@staticmethod
	def fromKolab(data):
		return KolabColor(data)

	def toKolab(self):
		return "#%02x%02x%02x" % (self.r, self.g, self.b) 	

class KolabBool(bool):
    def __init__(self, *arg):
        str.__init__(self, *arg)
    
    @staticmethod
    def fromKolab(data):
		if data == "True":
			return KolabBool(1)
		else:
			return KolabBool(0)
    
    def toKolab(self):
        return str(self).lower()


class KolabObject:
    def __init__(self, email=None):
        if email:
            etree = ElementTree.fromstring(email) 
            self.xmlTree= etree
            self.uuid = KolabString(etree.find("uid").text)
            self.creationDate = KolabDateTime(etree.find("creation-date").text)
            self.lastModificationDate = KolabDateTime(etree.find("last-modification-date").text)
        else:
    	    pass

def createObject(message):
    KolabObject()
