# -*- coding: utf-8 -*-

import datetime

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

class KolabDateTime:
    pass

class KolabColor:
    pass

class KolabBool:
    pass

class KolabObject:
    pass

def createObject(message):
    return KolabObject()
