# -*- coding: utf-8 -*-

import imaplib

class Connection:
    def __init__(self):
        pass

    def connect(self, username, password, server, port=None, use_ssl=False):
        imap = None
        if use_ssl:
            if port:
                imap = imaplib.IMAP4_SSL(server, port)
            else:
                imap = imaplib.IMAP4_SSL(server)
        else:
            if port:
                imap = imaplib.IMAP4(server, port)
            else:
                imap = imaplib.IMAP4(server)
        imap.login(username, password) 
        self.imap = imap
        

    def disconnect(self):
        self.imap.logout()  
    
def connect(username, password, server, port=None,  use_ssl=False):
    con = Connection()
    con.connect(username, password, server, port, use_ssl)
    return con
