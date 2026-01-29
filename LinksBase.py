import Interface as glParam
#----------------------------------------------
from datetime import datetime
import os

class LinksBase:
    def __init__(self):
        self.listOfPages_=[]
        self.listOfLinks_={}

    #////////////////////////////////////////////////
    #linkovi se upisuje iz liste imena linkova, fajl globalVars
        for name in glParam.imena_linkova.keys():
            self.listOfPages_.append(name)
            self.listOfLinks_[name]=glParam.imena_linkova[name]            
    #////////////////////////////////////////////////
