from pyparsing import Group, QuotedString, Suppress, OneOrMore, Word, nums, alphanums, Or, Keyword, Forward, ZeroOrMore

class ImapParsing:
    def __init__(self, imap):
        self.imap = imap

    def select(self, folder):
        """Select Imap folder; returns number of messages within folder"""

        typ, data = self.imap.select(folder)
        assert typ == 'OK'
        return data[0]

    def mlist(self, filter=None):
        if filter:
            assert type(filter) == tuple
            typ, data = self.imap.search(None, '(HEADER ' + ' '.join(filter) + ')')
            assert typ == 'OK'
        else:
            typ, data = self.imap.search(None, 'ALL')
            assert typ == 'OK'

        return data[0].split()

    def get(self, id):
        return ImapMail(self.imap, id)


class ImapMail:
    def __init__(self, imap, id):
        self.imap = imap
        self.open(id)

    def open(self, id):
        self.id = id
        item = 'BODY'
        typ, data = self.imap.fetch(id, '(' + item + ')')
        assert typ == 'OK'

        inline_parse = Forward()
        inline_parse << Suppress("(") + Group(OneOrMore(Or([Keyword("NIL"), QuotedString('"'), Word(nums), inline_parse ]))) + Suppress(")")
        parse = Word(nums) + Suppress("(") + Keyword(item) + Suppress("(") + Group(OneOrMore(inline_parse)) + ZeroOrMore(Or([Keyword("NIL"), QuotedString('"'), Word(nums)])) +  Suppress(")") + Suppress(")")
        p = parse.parseString(data[0])

        #print data[0]
        #print p
        #print

        self.attachment = []
        for i in p[2]:
            #while 'NIL' in i:
            #    i.remove('NIL')

            a = {
                'type'          : '/'.join(i[0:2]).lower(),
                i[2][0].lower() : i[2][1],
            }
                
            self.attachment.append(a)


    def listBodies(self, filter=None):
        result = []
        if filter:
            n = 1
            assert type(filter) == tuple
            for i in self.attachment:
                if i.has_key(filter[0]) and i[filter[0]] == filter[1]:
                    result.append(n)
                n += 1
            return result
        else:
            result = range(1, len(self.attachment) + 1)
            return result

    def getBody(self, id=1):
        assert id > 0
        return self.imap.fetch(id, '(BODY.PEEK[%i])' % id)[1][0]

    def getBodyHeader(self, id=1):
        assert id > 0
        a = {}

        typ, data = self.imap.fetch(id, '(BODY.PEEK[%i.MIME])' % id)
        tmp = data[0][1].splitlines()
        for i in tmp:
            if i == '':
                continue

            if i.startswith(' '):
                b = i.partition('=')
            else:
                b = i.partition(':')
            a[b[0].strip()] = b[2].strip().strip(';"')
        return a

