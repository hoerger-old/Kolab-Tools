# -*- coding: utf-8 -*-

from pyparsing import Group, QuotedString, Suppress, OneOrMore


class Annotations:
    A_CLASS    = '/vendor/kolab/folder-type'
    A_KEY      = 'value.shared'


class Parse:
    @staticmethod
    def foldersByAnnotation(folderlist, type):
        result = []
        parse = QuotedString('"') + QuotedString('"') + Suppress("(") + Group(OneOrMore(QuotedString('"'))) + Suppress(")")

        for folder in folderlist:
            tmp = parse.parseString( folder )
            if type in tmp[2][1]:
                result.append(tmp[0])

        return result
            

    @staticmethod
    def folderAnnotation(folder):
        pass
