# -*- coding: utf-8 -*-

from pyparsing import Group, QuotedString, Suppress, OneOrMore
from kolab.utils.annotations import Annotations
from kolab.utils.annotations import Parse
from kolab.resources import Calendar

type2resource = {
    'event'  : Calendar,
    'task'   : None,
    'journal': None,
    'contact': None,
    'note'   : None,
    }

class ResourceManager:
    def __init__(self, connection):
        self.connection = connection


    def listResources ( self, type ):
        "get folders with annotation type"

        # maybe add some caching functionality

        tmp = self.connection.imap.getannotation('*', Annotations.A_CLASS, '("%s")' % Annotations.A_KEY)[1]
        resource_folders = Parse.foldersByAnnotation( folderlist=tmp, type=type )

        return resource_folders

    def getResources ( self, type ):
        resources = []

        for i in self.listResources(type):
            resources.append(type2resource[type](self.connection, i))

        return resources
            
