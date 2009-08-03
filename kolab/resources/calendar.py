# -*- coding: utf-8 -*-

from resource import Resource

class Calendar(Resource):
    type = "event"

    def __init__(self, folder):
        self.folder = folder
