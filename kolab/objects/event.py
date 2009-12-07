import object

class KolabEvent(object.KolabObject):
    def __init__(self, email=None):
        object.KolabObject.__init__(self, email)

        summary = self.xmlTree.find("summary")
        if summary==None:
            summary = ""
        self.summary=object.KolabString.fromKolab(summary.text)

        location = self.xmlTree.find("location")
        if location==None:
            location = ""
        self.location=object.KolabString.fromKolab(location.text)
       
        class emailTupel:
            def __init__(self,display_name, smtp_address): 
                if display_name==None: display_name=""     
                if smtp_address==None: smtp_address=""     
                self.display_name=object.KolabString.fromKolab(display_name)
                self.smtp_address=object.KolabString.fromKolab(smtp_address)

        self.creator = emailTupel(self.xmlTree.find("creator/display-name").text\
                                 self.xmlTree.find("creator/smtp_address").text
        self.organizer = emailTupel(self.xmlTree.find("organizer/display-name").text\
                                   self.xmlTree.find("organizer/smtp_address").text

        start_date = self.xmlTree.find("start-date")
        if location==None:
            raise object.KolabObjectFormatError("start-date not present", "Event")     
        self.start_date=object.DateOrDateTime(start_date.text)

        alarm = self.xmlTree.find("alarm")
        if alarm!=None:
            self.alarm=object.KolabString.fromKolab(alarm.text)

