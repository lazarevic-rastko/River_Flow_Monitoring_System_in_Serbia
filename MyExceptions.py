from abc import abstractmethod
import Interface as glParam
#------------------------------
from datetime import datetime
import os

#neki specificni izuzeci moguci u sistemu
#opis svakog izuzetka je dat u njegovoj povratnoj informaciji

#upisuje poruku izuzetka u specifican fajl history.txt
#prisutan u svakoj klasi specificnog izuzetka
#pri hvatanju/obradi istog se vrsi ispis u fajl

#funkcija koja pohranjuje istoriju
def writeInHistory(strIn,filePath):
    os.makedirs(os.path.dirname(filePath), exist_ok=True) #prolazi kroz direktorijume i dodaje foldere koji nedostaju
    try:
        
        with open(filePath,"a",encoding="utf-8") as historyFile:
            if strIn == 60*"-":
                line=strIn+"\n"
                historyFile.write(line)
                return
                
            date = datetime.now().strftime("[%d.%m.%Y %H:%M:%S]")
            line = strIn + " -> " + date + "\n"
            historyFile.write(line)
            
    except Exception as e:
        print("Fajl istorije rada nije otvoren! Problem nije upisan u bazu!")
        print(str)

#/////////////////////////////////////////
#Osnovni tipovi izuzetaka
#/////////////////////////////////////////

class SistemskiProblem(Exception):
    def __init__(self,readerName):
        self.readerName_ = readerName
    def writeInHistory(self):
        writeInHistory("Opis problema koji narusava rad",glParam.istorijaSistema)   
        
class ReaderIsNotCreatedProperly(Exception):
    def __init__(self,readerName):
        self.readerName_ = readerName
    def writeInHistory(self):
        writeInHistory("Citac "+ self.readerName_ +" tj. njegov fajl nije ispravno kreiran!",glParam.istorijaSistema)   
class UpdateReaderStartError(Exception):
    def __init__(self,readerName):
        self.readerName_ = readerName
    def writeInHistory(self):
        writeInHistory("Citac "+ self.readerName_ +" tj. njegov fajl nije ispravno prondjen ili otvoren pri aktivaciji aplikacije! Program je prekinut.",glParam.istorijaSistema)
class UpdateCompletedError(Exception):
    def __init__(self,readerName):
        self.readerName_ = readerName
    def writeInHistory(self):
        writeInHistory("Proces citanja je izvrsen, ali citac "+ self.readerName_ +" nije ispravno otvoren za identifikovanje kraja procesa! Program se dalje izvrsava regularno!",glParam.istorijaSistema)

#/////////////////////////////////////////       
#Problemi prilikom otvaranja tj. prelaska sa jedne 
#web stranice na drugu
class FirstLinkError(Exception):
    def writeInHistory(self):
        writeInHistory("Greska pri otvaranju prve WEB stranice (tabela stanica)! Program je prekinut!",glParam.rhmzIstorijaRada)
class SecondLinkError(Exception):
    def __int__(self,value=""):
        super().__init__(value)
    def writeInHistory(self):
        writeInHistory(f"Greska pri otvaranju {self.args[0]} stranice!\nSajt nije dostupan-ostaje na pocetnoj stranici RHMZ\nProgram se nastavlja.",glParam.rhmzIstorijaRada)
class ThridLinkError(Exception):
    def writeInHistory(self):
        writeInHistory("Greska pri citanju nacina izvestavanja!",glParam.rhmzIstorijaRada)
        
#/////////////////////////////////////////       
#Problemi prilikom ?itanja podataka
#npr. parsiranje
class ReadingInfOneError(Exception):
    def writeInHistory(self):
        writeInHistory(f"Prisutna greska pri citanju vodostaja {self.args[0]}!",glParam.rhmzIstorijaRada)
class ReadingInfTwoError(Exception):
    def writeInHistory(self):
        writeInHistory(f"Prisutna greska pri citanju promene vodostaja {self.args[0]}!",glParam.rhmzIstorijaRada)
class ReadingInfThreeError(Exception):
    def writeInHistory(self):
        writeInHistory(f"Prisutna greska pri citanju protoka vode {self.args[0]}!",glParam.rhmzIstorijaRada)
class ReadingInfFourError(Exception):
    def writeInHistory(self):
        writeInHistory(f"Prisutna greska pri citanju temperature {self.args[0]}!",glParam.rhmzIstorijaRada)
        
#/////////////////////////////////////////       
#Stanice
class StattionFileNotCreated(Exception):
    def __int__(self,value=""):
        super().__init__(value)
    def writeInHistory(self):
        writeInHistory(f"Greska pri kreiranju fajla stanice: {self.args[0]}.",glParam.rhmzIstorijaRada)
class StattionFileNotOpen(Exception):
    def __int__(self,value=""):
        super().__init__(value)
    def writeInHistory(self):
        writeInHistory(f"Greska pri otvaranju fajla stanice: {self.args[0]}.",glParam.rhmzIstorijaRada)
class NotOnSite(Exception):
    def __int__(self,value=""):
        super().__init__(value)
    def writeInHistory(self):
        writeInHistory(f"Stanica {self.args[0]} nije pronadjena na sajtu.",glParam.rhmzIstorijaRada)


#/////////////////////////////////////////
#Izuzeci za RHMZ.RS
#/////////////////////////////////////////
class RHMZRSnekiIzuzetak(Exception):
    def __int__(self,value=""):
        super().__init__(value)
    def writeInHistory(self):
        writeInHistory("Ovo je opis izuzetka",glParam.rhmzRsIstorijaRada)


#
#
#
#