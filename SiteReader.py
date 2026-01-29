from re import L
from MyExceptions import*
from RhmzReaderFunctions import extractWebPage,readWebPage
import Interface as glParam
#-----------------------------------------------------------
from datetime import datetime
from abc import ABC, abstractmethod
import os


#Klase čitača, svaka klasa definisace GLAVNU funkciju čitanja
#za jedan sajt

#Čitac stranica, a dalje kreću njegove specijalizacije
#trebalo da kreira novi fajl,
#ukoliko već ne postoji, za praćenje rada svakog čitača

class SiteReader(ABC):
    def __init__(self,ReaderName,*args):
        self.readerName_=ReaderName
        self.variables_=[]
           
        self.fileNamePattern_=""
        
        self.readerLink_=""
        self.variables_=list(args)

    def writeReaderFile(self,description=""):
        os.makedirs(os.path.dirname(self.fileNamePattern_), exist_ok=True) #prolazi kroz direktorijume i dodaje foldere koji nedostaju
        
        if not os.path.exists(self.fileNamePattern_):
            try:
                with open(self.fileNamePattern_, "w",encoding="utf") as readerFile:
                    
                    line=self.formatHeaderReaderFile(description)
                    readerFile.write(line)

            #//////////////////////////////////////////

            except Exception as e:
                raise ReaderIsNotCreatedProperly(self.readerName_)
            
    def updateReaderStart(self):
        #znak koji se upisuje u fajl da je čitač aktiviran
        try:
            with open(self.fileNamePattern_, "a",encoding="utf") as readerFile:
                
                date=datetime.now().strftime("[%d.%m.%Y %H:%M:%S]")
                readerFile.write("\nČITAČ AKTIVIRAN->"+date)

    #//////////////////////////////////////////      
        except Exception as e:
            raise UpdateReaderStartError(self.readerName_)
        
    def updateCompleted(self):
        #aktivira se ukoliko je čitav proces zavrsen (uspešno)
        try:
            with open(self.fileNamePattern_, "a",encoding="utf") as readerFile:
                
                date=datetime.now().strftime("[%d.%m.%Y %H:%M:%S]")
                readerFile.write("->AKCIJA ZAVRŠENA->"+date)

    #//////////////////////////////////////////
        except Exception as e:
            raise UpdateCompletedError(self.readerName_)    
    def KeybordInterupt(self):
        #aktivira se ukoliko je proces naglo okoncan
        try:
            with open(self.fileNamePattern_, "a",encoding="utf") as readerFile:
                
                date=datetime.now().strftime("[%d.%m.%Y %H:%M:%S]")
                readerFile.write("->POKUŠAJ NASILNOG OKONČANJA PROCESA->"+date)

    #//////////////////////////////////////////   
        except Exception as e:
            raise UpdateCompletedError(self.readerName_)     
        
    def formatHeaderReaderFile(self,description):
        #formatiranje naslova fajla za citac

        date = datetime.now().strftime("[%d.%m.%Y %H:%M:%S]")
        header = "Čitač sajta - " + self.readerName_ + ", uspešno kreiran " + date + "\n"
        
        lh=len(header)
        header += "-" * lh + "\n"+"Opis:\n"   
        header+=description
        header += "-" * lh + "\n"
        
        line = "Promenjive čitača: "
        line += ",".join(self.variables_)
        header += line
        
        return header


    #//////////////////////////////////////////
    #Neke get i set metode
    def getName(self):
        #vraca ime čitača
        return self.readerName_
    def getLink(self):
        #vraća link Web stranice
        return self.readerLink_
    def setLink(self,link=""):
        #postavlja link
        self.readerLink_=link
    def setFileNamePatern(self,filePath):
        self.fileNamePattern_=filePath
        
    #//////////////////////////////////////////
    #Apstraktne metode koje bi trebalo prevazići u svakom
    #od novih čitača
    @abstractmethod
    def startReading(self):
        pass
    
#//////////////////////////////////////////
#Čitac RHMZ sajta
class RHMZreader(SiteReader):
    def __init__ (self, ReaderName,*args):
        super().__init__(ReaderName,*args)
        #KREIRANJE FAJLA KOJI PRATI ISPRAVNOST RADA
        #ČITAČA I NOSI INFORMACIJE O ISTOM
        self.setFileNamePatern(glParam.izvestajRadaCitacaSajta)
        self.writeReaderFile(glParam.rhmzOpis)

        self.nextWebPages=[]
        self.nextPagesReduced=[]      
    
    #NAJVAZNIJA FUNKCIJA
    def startReading(self):
        #Pripreme za pocetak rada
        writeInHistory("Proces je započet!",glParam.rhmzIstorijaRada)
        self.updateReaderStart()
        
        self.nextWebPages=extractWebPage(self.readerLink_)
        self.nextPagesReduced=[[elem[1],elem[2]] for elem in self.nextWebPages];
        
        self.readWebPage(glParam.listaSvihStanica["Drina"],glParam.rezultatiSlivDrina)
        self.readWebPage(glParam.listaSvihStanica["Dunav"],glParam.rezultatiSlivDunav)
        self.readWebPage(glParam.listaSvihStanica["Kolubara"],glParam.rezultatiSlivKolubara)
        self.readWebPage(glParam.listaSvihStanica["Nišava"],glParam.rezultatiSlivNisava)
        
        self.updateCompleted()
        writeInHistory("Proces je okončan!",glParam.rhmzIstorijaRada)
        writeInHistory("-" * 60,glParam.rhmzIstorijaRada)
        

    def readWebPage(self,list=[],folderPath=""):
        for elem in self.nextWebPages:
            try:
                if [elem[1],elem[2]] in list:#provera da li je trenutna stanica u listi stanica od interesa
                    readWebPage(folderPath,elem[1],elem[2],elem[3],self.readerLink_,self.variables_); #poziva spoljasnju funkciju za citanje
                    
    #//////////////////////////////////////////
    #Detekcija nekih nepravilnosti u radu                                                                                  
            except KeyboardInterrupt:
                self.KeybordInterupt();
                writeInHistory("Program je naglo zaustavljen!\n"
                               "Moguce je da neke informacije nisu upisane\n")
                writeInHistory("-" * 60 + '\n');
            except UpdateCompletedError as e:
                e.writeInHistory();
            except SecondLinkError as e:
                e.writeInHistory();
        
	    #provera da li je stanica prisutna na sajtu

        for el in list:
            if el not in self.nextPagesReduced:
                e = NotOnSite(el[0]+"_"+el[1])
                e.writeInHistory()



class RHMZRSreader(SiteReader):
    def __init__ (self, ReaderName,*args):
        super().__init__(ReaderName,*args)
        
        self.setFileNamePatern(glParam.izvestajRadaCitacaSajtaRHMZRS)
        self.writeReaderFile(glParam.rhmzrsOpis)
        
    def startReading(self):
        self.updateReaderStart()

        writeInHistory("Proces je započet!",glParam.rhmzRsIstorijaRada)
        
        os.makedirs(os.path.dirname(glParam.korisniPodaci), exist_ok=True)
        with open(glParam.korisniPodaci, "a", encoding="utf-8") as file:
            file.write("inf1,inf2,inf3\n")
        
        writeInHistory("Proces je okoncan!",glParam.rhmzRsIstorijaRada)
        self.updateCompleted()