from MyExceptions import *
#--------------------------
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os
import re

NULL_CONST = 999
ZERO_CONST = 0

#ovo su specificne funkcinalnosti za citac RHMZ, koja ce biti koriscene u RHMZreader klasi citaca
#slican fajl bi trebalo formirati za neki drugi citac, ukoliko dodje do prosirivanja sistema

def extractWebPage(pageUrl=""):
#iščitava sa polaznog sajta važne elemnte za dalje čitanje i formiranje narednih linkova
#index,ime stanice, sliv i parametar za naredni link

    try:
        response=requests.get(pageUrl);#pristup sadržaju web stranice
        stations=[]
        if response.status_code==200:#provera da li je pristup bio uspešan
            soup = BeautifulSoup(response.text, 'html.parser');#obrada i parsiranje HTML sourca web stranice
            tmp=soup.find_all('tr'); #pronalazi tagove tabele tj. <tr></tr> i pakuje ih u listu redom
            
            #/////////////////////////////////////////
            for i in range(2,len(tmp)-3):
                try:
                    #parsiranje u svrhu izdvajanja informacija
                    l = tmp[i].get_text().strip()
                    l = l.replace('\n','-').replace("\xa0",'')
                    k = l.split(sep="-")
                    m = str(tmp[i])
                    n = m.split('\n')
                    
                    #ovde biti oprezan da li je sajt na cirilici ili na latinici
                    #ako je cirilica  o=n[2].split('"')[3]

                    o = n[3].split('"')[3]
                    k.append(o)
                    k = [el for el in k if el != ""]
            #//////////////////////////////////////////

                except Exception as e:
                    continue
                else:
                    stations.append(k)
        else:
            raise FirstLinkError
    except Exception as e:
        raise FirstLinkError
    return stations

def readWebPage(folderPath,stationName="", river="", newLinkWord="",pageUrl="",Variables=[]):
#koristi polazni link, i dodatne parametre dobijene iz extractWebPage(), formira novi link i ulazi u njega
#poziva druge funkcije za citanje razlicitih podataka sa web stranice

    os.makedirs(folderPath, exist_ok=True) #prolazi kroz direktorijume i dodaje one koji nedostaju
    
    newUrl=pageUrl[0:len(pageUrl)-9] + newLinkWord
    try:
        response = requests.get(newUrl);#slican postupak kao u gornjoj funkciji
        if response.status_code==200:
            soup = BeautifulSoup(response.text, 'html.parser')
            tmpTr = soup.find_all('tr')
            tmpOne = str(tmpTr[12]).split('\n')
            tmpH1=soup.find_all('h1')
            reportStat=1
            wayOfReport="NULL"
            try:
            #////////////////////////////

                wayOfReport=openAndReadNextPage(str(tmpH1[0]),pageUrl) #iscitava nacin izvestavanja sa sajta za datu stanicu
                                                                       #koristeci odgovarajacu <h1>...</h1>tag sa stranice
            #////////////////////////////                              
            except ThridLinkError as e:
            #////////////////////////////  
              
                reportStat=2;              #promena statusa (o znacenju statusa parametara videti u opisu citaca, fajl RHMZ.txt)
                e.writeInHistory();        #ispis istorije

            dateFromSite=findSiteDate(str(tmpTr[8]));#cita datum sa sajta 
            result=readInformations(tmpOne,stationName,river); #cita parametre (variables)
            
            #////////////////////////////
            try:
            #////////////////////////////
                
                writeStationFile(folderPath,stationName,river,Variables,dateFromSite,result[0],result[4],#ova funkcija vrsi upis u fajl svih informacija
                             result[1],result[5],result[2],result[6],result[3],result[7],     #koje smo vec procitali
                             wayOfReport,reportStat)
                
            #////////////////////////////
            except StattionFileNotCreated as e:
                e.writeInHistory()
            except StattionFileNotOpen as e:
                e.writeInHistory()
        else:
            raise SecondLinkError(stationName+"_"+river)
    except Exception as e: 
        
        #ova situacija se uspostavlja ukoliko prelaz sa pocetne stranice na
        #narednu stranicu (stranicu stanice) nije obavljen adekvatno
        #te su u skladu sa tim i odgovarajuci argumenti i dalje prosledjivanje izuzetka

        writeStationFile(folderPath,stationName, river, Variables, "NULL", NULL_CONST, ZERO_CONST,
                         NULL_CONST,ZERO_CONST, NULL_CONST, ZERO_CONST, NULL_CONST, ZERO_CONST, "NULL", ZERO_CONST)
        
        raise SecondLinkError(stationName+"_"+river)

def readInfTwoAndFour(strLine=""):
#pomoćna funkcija za parsirane i čitanje, i to drugog i četvrtog parametra,
#koje su zbog prirode
#stranice sa koje se čitaju slične

    tmp=strLine.split("\xa0")
    if len(tmp)<2:
        return 0
    tmpOth=tmp[1].split('<')[0]
    if tmpOth=='-' or tmpOth=='*' or tmpOth=='' :
        return NULL_CONST
    result=float(tmpOth)
    return result

def readInformations(lst=[],stattion="",river=""):
#stranica koja isporučuje parametre od interesa
#objedinjuje funkciju readInfTwoAndFour sa dodatnim parsiranjima
#999 ce se prevesti NULL vrednost u daljem toku

    statOne=statTwo=statThree=statFour=1
    outMess=stattion+"_"+river
    
    #////////////////////////////
    # inf ONE
    try:
        helper = lst[2].split('<')[0]
        if helper == '*' or helper == '-' or helper == '':
            infOne = NULL_CONST
        else:
            infOne = float(lst[2].split('<')[0])
    except Exception as e:
        statOne = 2
        infOne = NULL_CONST;a = ReadingInfOneError(outMess);a.writeInHistory()
    #////////////////////////////
    # inf TWO
    try:
        infTwo = readInfTwoAndFour(lst[3])
    except Exception as e:
        statTwo = 2
        infTwo = NULL_CONST
        a = ReadingInfTwoError(outMess);a.writeInHistory()
    #////////////////////////////
    # inf Three
    try:
        infThree1 = lst[4].split('>')[1].split('<')[0]
        if infThree1 == "" or infThree1 == "-" or infThree1 == "*":
            infThree = NULL_CONST
        else:
            infThree = float(infThree1)
    except Exception as e:
        statThree = 2
        infThree = NULL_CONST
        a = ReadingInfThreeError(outMess);a.writeInHistory()
    #////////////////////////////
    # inf four
    try:
        infFour = readInfTwoAndFour(lst[5])
    except Exception as e:
        statFour = 2
        infFour = NULL_CONST
        a = ReadingInfFourError(outMess);a.writeInHistory()
        
    return infOne,infTwo,infThree,infFour,statOne,statTwo,statThree,statFour

def prepare(inStr=""):
    #otklanje iz satrigna karaktere koji nisu slova i brojevi (space čuva)
    #otklanja spoljnje beline
    #pojačava robusnost i stabilnost prilikom kreiranja i otvaranja fajlova pojedinih stanica

    #ovo je kad je je sajt na cirilici
    #out=re.sub(r'[^а-џЈ-Ш0-9\s]', '', inStr)
    out=inStr.strip()
    out=out.upper()
    out=re.sub(r"\s+", "_", out)
    return out

def writeStationFile(folderPath,stationName="", river="", variables=[], readDate="", infOne=0, statOne=1, infTwo=0, statTwo=1, infThree=0, statThree=1, infFour=0, statFour=1, reportWay="",reportStat=0):
    date = datetime.now().strftime("[%d.%m.%Y %H:%M:%S]")
    dateWithoutTime=datetime.now().strftime("%d.%m.%Y.")
    
    stationName=prepare(stationName)
    river=prepare(river)
    
    stationPattern=stationName + "_" + river + ".txt"
    filePath = os.path.join(folderPath, stationPattern)
    
    #////////////////////////////
    if not os.path.exists(filePath):
        try:
            #prvo formiranje fajla za stanice
            with open(filePath, "w", encoding="utf-8") as fileOne:
                
                header = formatHeaderStationFile(stationName,river,variables,date)
                fileOne.write(header)     
                
        except Exception as e:
            raise StattionFileNotCreated(stationName+"_"+river)
    
    try:
        #upis u fajl relevantnih parametara i informacija
        with open(filePath, "a", encoding="utf-8") as file:
            
            #obrada vrednosti
            infOne="NULL" if infOne==NULL_CONST else str(infOne);
            infTwo = "NULL" if infTwo == NULL_CONST else str(infTwo);
            infThree = "NULL" if infThree == NULL_CONST else str(infThree);
            infFour = "NULL" if infFour == NULL_CONST else str(infFour)
            dateStat=1 if dateWithoutTime == readDate else 0;
            dateStat=2 if readDate=="NULL" else dateStat;

            line = formatText(infOne,statOne,infTwo,statTwo,infThree,statThree,infFour,statFour,reportWay,reportStat,date,dateStat)
            file.write(line)
            
    except Exception as e:
        raise StattionFileNotOpen(stationName+"_"+river)
    
def openAndReadNextPage(h1Line="",originalLink=""):
    #ova funkcija se koristi da nas sa stranice specificne stanice
    #pošalje na stanicu koja nosi informaciju o načinu izveštavanja
    #pristup je sličan 1.rekonstrukcija link 2.preuzimanje HTML sourca 3.parsiranje do dobijanja traženog podatka

    wordOne=h1Line.split("href=\"../")[1]
    wordTwo=wordOne.split("\"")[0]
    newUrl = originalLink[0:len(originalLink) - 20]+wordTwo
    
    #//////////////////////////////////////////
    try:
        response = requests.get(newUrl)
        if response.status_code == 200:
            final=""
            soup = BeautifulSoup(response.text, 'html.parser')
            tmpTr = soup.find_all('tr')
            prepOne = str(tmpTr[20]).split('\n')
            prepTwo = prepOne[2]
            prepThree = prepTwo.split('>')[1]
            final = str(prepThree.split('<')[0])
            if final == "":
                final = "NULL"
            return final
    #//////////////////////////////////////////

        else:
            raise ThridLinkError
    except Exception as e:
        raise ThridLinkError
    
def findSiteDate(dateLine=""):
    #čita datum koji je upisan na stranici
    wordOne=dateLine.split("\n")[1]
    wordTwo=wordOne.split(",")[1]
    wordThree=wordTwo.split("<")[0].strip()
    return wordThree

def formatText(infOne,statOne,infTwo,statTwo,infThree,statThree,infFour,statFour,reportWay,reportStat,date,dateStat):
    #formitira podatke

    line=""
    line = infOne + "("+str(statOne)+"),"
    line+= infTwo + "("+str(statTwo)+"),"
    line+=infThree+"("+str(statThree)+"),"
    line+=infFour+"("+str(statFour)+"),"
    line+=date+"("+str(dateStat)+"),"
    line+=reportWay+"("+str(reportStat)+")\n"
    
    return line

def formatHeaderStationFile(stationName,river,variables,date):
    #formatira naslovni deo fajla svake stanice    

    headText = stationName + "_" + river + "\n" + "Uspesno kreiran  " + date + "\n"
    line="(status),".join(variables)
    line+="(status),datum pracenja(status)"
    line += ",nacin pracenja(status)\n"
    
    return headText+line