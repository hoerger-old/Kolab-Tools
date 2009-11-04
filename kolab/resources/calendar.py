# -*- coding: utf-8 -*-

from resource import Resource

class Calendar(Resource):
    type = "event"

    def readItem(self, id):
        # its possible that non unique id of message changes while this object is active
        # so we should maybe use uuid?
        self.imapp.select(self.folder)
        m = self.imapp.get(id)
        return m.getBody(m.listBodies(filter=('type','application/x-vnd.kolab.event'))[0])

    def listItems(self, filter=None):
        self.imapp.select(self.folder)
        return self.imapp.mlist(filter=('X-Kolab-Type', 'application/x-vnd.kolab.event'))
