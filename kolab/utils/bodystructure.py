# -*- coding: utf-8 -*-

from pyparsing import Group, QuotedString, Suppress, OneOrMore, Word, nums, alphanums, Or


class Annotations:
    A_CLASS    = '/vendor/kolab/folder-type'
    A_KEY      = 'value.shared'


class Parse:
    @staticmethod
    def foldersByAnnotation(folderlist, type):
        result = []
        # parse this 3 (BODYSTRUCTURE (("TEXT" "PLAIN" ("CHARSET" "iso-8859-1") NIL NIL "QUOTED-PRINTABLE" 539 12 NIL NIL NIL NIL)("APPLICATION" "X-VND.KOLAB.EVENT" ("NAME" "kolab.xml") NIL NIL "7BIT" 679 NIL ("ATTACHMENT" ("FILENAME" "kolab.xml")) NIL NIL) "MIXED" ("BOUNDARY" "Boundary-00=_H2YnIG887ejM4hn") NIL NIL NIL))


"""

3 
(
    BODYSTRUCTURE 
    (
        (
            "TEXT"
            "PLAIN" 
            (
                "CHARSET"
                "iso-8859-1"
            )
            NIL
            NIL
            "QUOTED-PRINTABLE" 
            539 
            12 
            NIL 
            NIL 
            NIL 
            NIL
        )
        (
            "APPLICATION" 
            "X-VND.KOLAB.EVENT" 
            (
                "NAME" 
                "kolab.xml"
            ) 
            NIL 
            NIL 
            "7BIT" 
            679 
            NIL 
            (
                "ATTACHMENT" 
                (
                    "FILENAME" 
                    "kolab.xml"
                )
            ) 
            NIL 
            NIL
        ) 
        "MIXED" 
        (
            "BOUNDARY" 
            "Boundary-00=_H2YnIG887ejM4hn"
        ) 
        NIL 
        NIL 
        NIL
    )
)

"""
        parse = Suppress(Word(nums)) + Suppress("(") + Group(OneOrMore( Suppress("(") + Group(OneOrMore(Word(printables))) + Suppress(")") )) + Suppress(")")

        for folder in folderlist:
            tmp = parse.parseString( folder )
            if type in tmp[2][1]:
                result.append(tmp[0])

        return result
            

    @staticmethod
    def folderAnnotation(folder):
        pass
