#---------------------------------------------------------------------------------------------
#LinkBase podesavanja
#---------------------------------------------------------------------------------------------

imena_linkova = {
    "RHMZ": "https://www.hidmet.gov.rs/latin/hidrologija/izvestajne/index.php",
    "RHMZRS":"https://www.hidmet.gov.rs/latin/hidrologija/izvestajne/index.php"
    }

#---------------------------------------------------------------------------------------------
#RHMZreader - podešavanja
#---------------------------------------------------------------------------------------------

#opis citaca
rhmzOpis = """Parametar - Znacenje statusa
NULL - nije prisutna numericka vrednost
Vodostaj(cm): 0-nije bilo moguce otvoriti stranicu za citanje; 1-ispravna vrednost; 2-stranica je bilo moguce otvoriti, ali su prilikom citanja nastali problemi
Promena vodostaja(cm): 0-nije bilo moguce otvoriti stranicu za citanje; 1-ispravna vrednost; 2-stranica je bilo moguce otvoriti, ali su prilikom citanja nastali problemi
Proticaj vode (m3/s): 0-nije bilo moguce otvoriti stranicu za citanje; 1-ispravna vrednost; 2-stranica je bilo moguce otvoriti, ali su prilikom citanja nastali problemi
Temperatura vode(оC): 0-nije bilo moguce otvoriti stranicu za citanje; 1-ispravna vrednost; 2-stranica je bilo moguce otvoriti, ali su prilikom citanja nastali problemi
Datum: 0-stranicu je bilo moguce ucitati, a datumi se ne poklapaju; 1-stranicu je bilo moguce ucitati, a datumi se poklapaju; 2-stranicu nije bilo moguce otvoriti, pa citanje datuma nije bilo moguce
Nacin izvestavanja: 0-nije bilo moguce otvoriti stranicu za citanje; 1-ispravna vrednost\n"""


#lista stanica koje pravimo po slivovima
listaStanicaSlivaDrina =   [["BAJINA BAŠTA", "DRINA"], ["RADALJ", "DRINA"], ["BADOVINCI", "DRINA"], ["BRODAREVO", "LIM"], 
                ["PRIJEPOLJE", "LIM"], ["PRIBOJ", "LIM"], ["PRIJEPOLJE", "MILEŠEVKA"], ["BISTRICA", "BISTRICA"], 
                ["ČEDOVO", "VAPA"], ["ZAVLAKA", "JADAR"], ["LEŠNICA", "JADAR"]]
listaStanicaSlivaDunav =  [["BEZDAN", "DUNAV"], ["APATIN", "DUNAV"], ["BOGOJEVO", "DUNAV"], ["BAČKA PALANKA", "DUNAV"], ["NOVI SAD", "DUNAV"], 
                ["SLANKAMEN", "DUNAV"], ["ZEMUN", "DUNAV"], ["PANČEVO", "DUNAV"], ["SMEDEREVO", "DUNAV"], ["BANATSKA PALANKA", "DUNAV"],
                ["VELIKO GRADIŠTE", "DUNAV"], ["GOLUBAC", "DUNAV"], ["DONJI MILANOVAC", "DUNAV"], ["BRZA PALANKA", "DUNAV"], 
                ["PRAHOVO", "DUNAV"], ["NOVI KNEŽEVAC", "TISA"], ["SENTA", "TISA"], ["PADEJ", "TISA"], ["NOVI BEČEJ", "TISA"],
                ["BRANA NOVI BEČEJ GV", "TISA"], ["BRANA NOVI BEČEJ DV", "TISA"], ["TITEL", "TISA"], ["VRBICA", "ZLATICA"], 
                ["PADEJ USTAVA", "ZLATICA"], ["FEKETIĆ", "KRIVAJA"], ["HETIN", "STARI BEGEJ"], ["SRPSKI ITEBEJ GV", "PLOVNI BEGEJ"],
                ["SRPSKI ITEBEJ DV", "PLOVNI BEGEJ"], ["KLEK", "PLOVNI BEGEJ"], ["JAŠA TOMIĆ", "TAMIŠ"], ["SEČANJ", "TAMIŠ"],
                ["PANČEVO", "TAMIŠ"], ["NOVI BEČEJ USTAVA", "DTD"], ["KAJTASOVO USTAVA GV", "DTD"], ["KAJTASOVO USTAVA DV", "DTD"],
                ["KUSIĆ", "NERA"], ["VRAČEV GAJ", "NERA"], ["MARKOVIĆEVO", "BRZAVA"], ["KONAK", "BRZAVA"], ["VATIN", "MORAVICA"],
                ["VRŠAC", "MESIĆ"], ["KUŠTILJ", "KARAŠ"], ["DOBRIČEVO", "KARAŠ"], ["ŽAGUBICA", "MLAVA"], ["GORNJAK", "MLAVA"],
                ["VELIKO SELO", "MLAVA"], ["BRATINAC", "MLAVA"], ["KULA", "VITOVNICA"], ["KUČEVO", "PEK"], ["KUSIĆE", "PEK"],
                ["CRNAJKA", "CRNAJKA"], ["CRNAJKA", "ŠAŠKA"], ["RIĐICA", "PLAZOVIĆ"]]
listaStanicaSlivaKolubara = [["VALJEVO", "KOLUBARA"], ["SLOVAC", "KOLUBARA"], ["BELI BROD", "KOLUBARA"], ["DRAŽEVAC", "KOLUBARA"],
                ["OBRENOVAC", "KOLUBARA"], ["SEDLARI", "JABLANICA"], ["BELO POLJE", "OBNICA"], ["DEGURIĆ", "GRADAC"], 
                ["MIONICA", "RIBNICA"], ["BOGOVAĐA", "LJIG"], ["ZEOKE", "PEŠTAN"], ["KOCELJEVA", "TAMNAVA"], 
                ["ĆEMANOV MOST", "TAMNAVA"], ["UB", "UB"]]
listaStanicaSlivaNisava = [["NIŠ","NIŠAVA"],["RADIKINA BARA","KUTINSKA"],["BELA PALANKA","NIŠAVA"],["STANIČENJE","TEMSKA"],
                ["VISOČKA RŽANA","DOJKINAČKA"],["IZATOVAC","VISOČICA"],["PIROT","NIŠAVA"],["BRAĆEVCI","VISOČICA"],
                ["TRNSKI ODOROVCI","JERMA"],["MRTVINE","GABERSKA"],["DIMITROVGRAD","NIŠAVA"]]
listaSvihStanica={"Drina": listaStanicaSlivaDrina,"Dunav":listaStanicaSlivaDunav,"Kolubara": listaStanicaSlivaKolubara, "Nišava":listaStanicaSlivaNisava }

#OVDE NISTA NE UPISIVATI!
istorijaSistema = None

izvestajRadaCitacaSajta=None
rhmzIstorijaRada = None
rezultatiSlivDrina = None
rezultatiSlivDunav = None
rezultatiSlivKolubara = None
rezultatiSlivNisava= None


#OVDE UPISIVATI, ide apsolutna putanju sa imenom fajla
#funkcija se pokrece na pocetku rada sistema i postavlja odgovarajuce putanje do FOLDERA



#---------------------------------------------------------------------------------------------
#RHMZ_RSreader - podešavanja
#---------------------------------------------------------------------------------------------

rhmzrsOpis="Ovo je opis mog citaca RHMZRS.\n"


rhmzRsIstorijaRada=None
izvestajRadaCitacaSajtaRHMZRS=None
korisniPodaci=None


#-----------------------------------------------------------------------------------------------
#Odabir operativnog sistema i prilagođavanje
#-----------------------------------------------------------------------------------------------
#odaberi operativni sistem na kojem se sistem pokreće: True za Linux, False za Windows
operatingSystem=False




#Inicijalizacija putanja prema odabiru operativnog sistema

def initializeAndSet():
    opSys=operatingSystem
    global istorijaSistema
    #RHMZ
    global izvestajRadaCitacaSajta
    global rhmzIstorijaRada
    global rezultatiSlivDrina 
    global rezultatiSlivDunav 
    global rezultatiSlivKolubara
    global rezultatiSlivNisava
    #
    global rhmzRsIstorijaRada
    global izvestajRadaCitacaSajtaRHMZRS
    global korisniPodaci
    
    if opSys:
        #upisi za Linux
        istorijaSistema = ""
        #RHMZ
        izvestajRadaCitacaSajta = ""
        rhmzIstorijaRada = ""
        istorijaSistema = ""
        
        rezultatiSlivDrina = ""
        rezultatiSlivDunav = ""
        rezultatiSlivKolubara = ""
        rezultatiSlivNisava = ""
        
        #RHMZRS
        rhmzRsIstorijaRada = ""
        izvestajRadaCitacaSajtaRHMZRS = ""
        korisniPodaci = ""

    else:
        #upisi za Windows
        istorijaSistema = "C:\\Users\\Korisnik\\Desktop\\Rezultati\\IstorijaSistema.txt"
        
        #RHMZ
        izvestajRadaCitacaSajta = "C:\\Users\\Korisnik\\Desktop\\Rezultati\\RezultatiRHMZ\\RezultatiRHMZ.txt"
        rhmzIstorijaRada = "C:\\Users\\Korisnik\\Desktop\\Rezultati\\RezultatiRHMZ\\IstorijaRHMZ.txt"
        istorijaSistema = "C:\\Users\\Korisnik\\Desktop\\Rezultati\\IstorijaSistema.txt"
        
        rezultatiSlivDrina="C:\\Users\\Korisnik\\Desktop\\Rezultati\\RezultatiRHMZ\\Slivovi\\SlivDrina"
        rezultatiSlivDunav="C:\\Users\\Korisnik\\Desktop\\Rezultati\\RezultatiRHMZ\\Slivovi\\SlivDunav"
        rezultatiSlivKolubara="C:\\Users\\Korisnik\\Desktop\\Rezultati\\RezultatiRHMZ\\Slivovi\\SlivKolubara"
        rezultatiSlivNisava="C:\\Users\\Korisnik\\Desktop\\Rezultati\\RezultatiRHMZ\\Slivovi\\SlivNisava"
        
        #RHMZRS
        rhmzRsIstorijaRada = "C:\\Users\\Korisnik\\Desktop\\Rezultati\\RezultatiRHMZRS\\IstorijaRHMZRS.txt"
        izvestajRadaCitacaSajtaRHMZRS = "C:\\Users\\Korisnik\\Desktop\\Rezultati\\RezultatiRHMZRS\\RezultatiRHMZRS.txt"
        korisniPodaci = "C:\\Users\\Korisnik\\Desktop\\Rezultati\\RezultatiRHMZRS\\SlivVrbas\\VRBAS_VRBAS.txt"






