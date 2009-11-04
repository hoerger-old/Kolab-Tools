# -*- coding: utf-8 -*-

from kolab.utils.imapparsing import ImapParsing

class Resource:
    def __init__(self, connection, folder):
        self.connection = connection
        self.folder = folder

        self.imapp  = ImapParsing(connection.imap)
        self.imapp.select(folder)

    def __str__(self):
        return self.folder

    def readAll(self):
        pass

    def readItem(self, id):
        pass

    def writeAll(self):
        pass

    def writeItem(self):
        pass

    def listItems(self, filter=None):
        # have to set the folder each time an item is access because imap cursor could jump to another folder in the meantime
        self.imapp.select(self.folder)
        return self.imapp.mlist()
