from LinksBase import LinksBase
from MyExceptions import*
from SiteReader import RHMZreader,RHMZRSreader
import Interface as init
#-------------------------------------------
from typing import Dict #tipiziranje recnika


class Aplication:
    def __init__(self):
        try:
        #inicijalizacija promenjivih iz globalVars

            init.initializeAndSet()
            
        #////////////////////////////   

        #baza citaca u vidu recnika
            self.ReaderBase_: Dict[str,RHMZreader]={}
        #baza verifikovanih citaca u vidu liste - inicijalno prazna, ispunjava se aktivacijom funkcije updateVerifiedReaders(self)
            self.verifiedReaders_=[]
            
        #////////////////////////////

        #baza linkova u vidu objekta tipa LinksBase
            self.LinkBase_=LinksBase()
            
        #//////////////////////////// 
   
        ##DODAVANJE CITACA##
            self.ReaderBase_["RHMZ"] =RHMZreader("RHMZ","Vodostaj(cm)","Promena vodostaja(cm)","Proticaj vode(m3/s)","Temperatura vode(оC)")
            self.ReaderBase_["RHMZRS"] =RHMZRSreader("RHMZ","param1","param2","param3")
            #
            #
            #
            #

        #////////////////////////////

        #VERIFIKACIJA ČITAČA    
            self.updateVerifiedReaders()


        #detekcija mogucih problema tokom rada, i upis u fajl koji prati
        #istoriju rada
        except ReaderIsNotCreatedProperly as e:
            print(e)
            exit(1)
            
    def updateVerifiedReaders(self):
        #ime sajta se poklapa sa imenom citaca, smatramo da je citac verifikovan,
        #moze se desiti da sajtu fali citac, i obrnuto

        #////////////////////////////
           
        for key in self.ReaderBase_.keys():
            if key in self.LinkBase_.listOfPages_:
                link=self.LinkBase_.listOfLinks_[key]
                self.ReaderBase_[key].setLink(link)
                self.verifiedReaders_.append(self.ReaderBase_[key])
                
        #////////////////////////////   

    def activeAplication(self):
        #vrsi aktivaciju svakog verifikovanog citaca
        try:
            if len(self.verifiedReaders_)<=0:
                writeInHistory("Nema verifikovanih citaca!",init.istorijaSistema)
                return
             
            #////////////////////////////////////////////////

            writeInHistory("Proces je započet!",init.istorijaSistema)
            
            #aktivacija svih verifikovanih citaca
            for k in range(0,len(self.verifiedReaders_)):
                self.verifiedReaders_[k].startReading()   
                
            writeInHistory("Proces je okončan!",init.istorijaSistema)

            #////////////////////////////////////////////////

        #detekcija mogucih problema tokom rada, i upis u fajl koji prati

        except UpdateReaderStartError as e:
            e.writeInHistory()
            return
        except UpdateCompletedError as e:
            e.writeInHistory()
            
        #RHMZ-----------------------------------------------------
        except FirstLinkError as e:
            e.writeInHistory()
            return 
        finally:
            writeInHistory("-" * 60,glParam.istorijaSistema)
            
        #RHMZ.RS--------------------------------------------------