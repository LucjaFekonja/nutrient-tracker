import json
import datetime
import os

# *******************************************  OSEBNI PODATKI  ***********************************************
        
class Osebno(object):
    '''
    Izračun vseh kalorij, ogljikovih hidratov (g), proteinov (g)
    in maščob (g) glede na osebne podatke uporabnika.
    '''
    def __init__(self, teza, visina, starost, spol, aktivnost):
        self.teza = float(teza)
        self.visina = float(visina)
        self.starost = float(starost)
        self.spol = spol
        self.aktivnost = aktivnost

    def bmi(self):
        return round(self.teza / (self.visina) ** 2, 1)

    def bmr(self):
        if self.spol == 'M':
            return 88.362 + 13.397 * self.teza + 4.799 * self.visina - 5.677 * self.starost
        if self.spol == 'Ž':
            return 447.593 + 9.247 * self.teza + 3.098 * self.visina - 4.330 * self.starost

    def bmr_na_aktivnost(self):
        if self.aktivnost ==  'nič':
            return self.bmr() * 1.2
        if self.aktivnost == '1-2 dni':
            return self.bmr() * 1.375
        if self.aktivnost == '3-5 dni':
            return self.bmr() * 1.55
        if self.aktivnost == '6-7 dni':
            return self.bmr() * 1.725
        if self.aktivnost == '2-krat dnevno':
            return self.bmr() * 1.9

    def priporocene_cal(self):
        if self.bmi() < 18.5:
            return int(self.bmr_na_aktivnost()) + 500
        if 18.5 <= self.bmi < 25:
            return int(self.bmr_na_aktivnost())
        if self.bmi >= 25:
            return int(self.bmr_na_aktivnost()) - 500
    
    def priporocene(self):
        priporocene_mascobe = self.priporocene_cal() * 25 / 400
        priporoceni_ogljikovi = self.priporocene_cal() * 50 / 400
        priporoceni_proteini = self.priporocene_cal() * 25 / 400
        return (round(int(priporoceni_ogljikovi), 0), round(int(priporoceni_proteini), 0), round(int(priporocene_mascobe), 0))


# *******************************************  VODENJE EVIDENCE  ***********************************************

def seznam(niz):
    niz2 = niz.lstrip('\n')
    sez1 = niz2.split(';')
    sez2 = [st for st in sez1[1:]]
    return [sez1[0]] + sez2

slovar = dict()
with open("C:\\Lucija\\1.letnik fmf\\UVP\\nutrient-tracker\\hrana.txt", encoding="utf-8") as dat:
    for vrstica in dat:
        slovar.update( {seznam(vrstica)[0] : seznam(vrstica)[1:]} )

# _____________________________________________________________________________________________________________

class Sledilnik(Osebno):
    def __init__(self, id, teza, visina, starost, spol, aktivnost, datum=None):
        super().__init__(teza, visina, starost, spol, aktivnost)
        self.teza = teza
        self.visina = visina
        self.starost = starost
        self.spol = spol
        self.aktivnost = aktivnost
#        self.cal = 0
#        self.mascobe = 0
#        self.ogljikovi = 0
#        self.proteini = 0   
#        self.vse_cal = self.priporocene_cal()
#        self.vsi_ogljikovi = self.priporocene()[0]
#        self.vsi_proteini = self.priporocene()[1]
#        self.vse_mascobe = self.priporocene()[2]
        self.seznam_hrane = dict()
        self.seznam_vrednosti = dict([
            ('vse_cal', self.priporocene_cal()),
            ('vsi_oh', self.priporocene()[0]),
            ('vsi_pro', self.priporocene()[1]),
            ('vse_mas', self.priporocene()[2]),
            ('porabljene_cal', 0),
            ('porabljeni_oh', 0),
            ('porabljeni_pro', 0),
            ('porabljene_mas', 0),
            ('preostale_cal', self.priporocene_cal()),
            ('preostali_oh', self.priporocene()[0]),
            ('preostali_pro', self.priporocene()[1]),
            ('preostale_mas', self.priporocene()[2]),
            ])
        self.id = id
        self.datum = datum


    def dodaj(self, hrana, gram):
        """
        Funkcija k porabljenim doda vrednosti iz datoteke hrana.txt,
        od vseh priporočenih odšteje iste količine in
        doda navedeno hrano in grame na seznam_hrane.
        """
        a = Seznam()
        vrednosti = a.naredi_slovar_hrane()[hrana]
        self.dodaj_na_seznam_hrane(hrana, float(gram))

        self.seznam_vrednosti['porabljene_cal'] += float(vrednosti[0]) * gram / 100
        self.seznam_vrednosti['porabljeni_oh'] += float(vrednosti[1]) * gram / 100
        self.seznam_vrednosti['porabljeni_pro'] += float(vrednosti[2]) * gram / 100
        self.seznam_vrednosti['porabljene_mas'] += float(vrednosti[3]) * gram / 100
    
        self.seznam_vrednosti['preostale_cal'] -= float(vrednosti[0]) * gram / 100    
        self.seznam_vrednosti['preostali_oh'] -= float(vrednosti[1]) * gram / 100
        self.seznam_vrednosti['preostali_pro'] -= float(vrednosti[2]) * gram / 100
        self.seznam_vrednosti['preostale_mas'] -= float(vrednosti[3]) * gram / 100

        return self.seznam_vrednosti

    def izbrisi(self, hrana):
        """
        Funkcija od porabljenih odvzame vrednosti iz datoteke hrana.txt,
        k priporočenim doda iste količine in
        izbriše navedeno hrano in grame iz seznam_hrane.
        """
        if hrana in self.seznam_hrane:
            a = Seznam()
            vrednosti = a.naredi_slovar_hrane()[hrana]
            kolicina = self.seznam_hrane[hrana]
            self.seznam_vrednosti['porabljene_cal'] -= float(vrednosti[0]) * kolicina / 100
            self.seznam_vrednosti['porabljeni_oh'] -= float(vrednosti[1]) * kolicina / 100
            self.seznam_vrednosti['porabljeni_pro'] -= float(vrednosti[2]) * kolicina / 100
            self.seznam_vrednosti['porabljene_mas'] -= float(vrednosti[3]) * kolicina / 100

            self.seznam_vrednosti['preostale_cal'] += float(vrednosti[0]) * kolicina / 100
            self.seznam_vrednosti['preostali_oh'] += float(vrednosti[1]) * kolicina / 100
            self.seznam_vrednosti['preostali_pro'] += float(vrednosti[2]) * kolicina / 100
            self.seznam_vrednosti['preostale_mas'] += float(vrednosti[3]) * kolicina / 100
            
            self.izbrisi_iz_seznama_hrane(hrana)
            return self.seznam_vrednosti
        else:
            print('Navedene hrane niste dodali.')

    # ------------  Funkcije uporabljene zgoraj  ------------
    def dodaj_na_seznam_hrane(self, hrana, gram):
        if hrana in self.seznam_hrane:
            self.seznam_hrane[hrana] += gram
            return self.seznam_hrane
        else:
            return self.seznam_hrane.update( {hrana : gram} )

    def izbrisi_iz_seznama_hrane(self, hrana):
        del self.seznam_hrane[hrana]  

    def pokazi_seznam_hrane(self):
        return self.seznam_hrane

    # ------------  Funkcije uporabljene v naprej  ------------
#    def porabljeno(self):
#        return [self.cal, self.ogljikovi, self.proteini, self.mascobe]
#
#    def preostalo(self):
#        return [self.vse_cal, self.vsi_ogljikovi, self.vsi_proteini, self.vse_mascobe]
#
#    # Naredimo class object, na katerega se bomo sklicevali v drugih razredih
#    def slovar_vrednosti(self):
#        slovar = {
#            'porabljene_cal' : round(self.porabljeno()[0], 1),
#            'porabljeni_oh' : round(self.porabljeno()[1], 1),
#            'porabljeni_pro' : round(self.porabljeno()[2], 1),
#            'porabljene_mas' : round(self.porabljeno()[3], 1),
#            'preostale_cal' : round(self.preostalo()[0], 1),
#            'preostali_oh' : round(self.preostalo()[1], 1),
#            'preostali_pro' : round(self.preostalo()[2], 1),
#            'preostale_mas' : round(self.preostalo()[3], 1),
#            'vse_cal' : round(self.priporocene_cal(), 1),
#            'vsi_oh' : round(self.priporocene()[0], 1),
#            'vsi_pro' : round(self.priporocene()[1], 1),
#            'vse_mas' : round(self.priporocene()[2], 1),
#        }
#        return slovar
    
    def slovar_dneva(self):
        slovar = {
            'teza' : self.teza,
            'visina' : self.visina,
            'starost' : self.starost,
            'spol' : self.spol,
            'aktivnost' : self.aktivnost,
            'datum' : self.datum,
            'id_dneva' : self.id,
            'hrana' : self.seznam_hrane,
            'seznam_vrednosti' : self.seznam_vrednosti
        }
        return slovar   

    @classmethod
    def object_sledilnik(cls, slovar):
        teza = slovar['teza']
        visina = slovar['visina']
        starost = slovar['starost']
        spol = slovar['spol']
        aktivnost = slovar['aktivnost']
        datum = slovar['datum']
        sledilnik = cls(id, teza, visina, starost, spol, aktivnost, datum)
        sledilnik.id = slovar['id_dneva']
        sledilnik.seznam_hrane = slovar['hrana']
        sledilnik.seznam_vrednosti = slovar['seznam_vrednosti']
        return sledilnik


# **********************************************  UPORABNIK  **************************************************

class Uporabnik():
    def __init__(self, ime, geslo):
        self.ime = ime
        self.geslo = geslo
        self.id_dneva = 0
        self.seznam_dni = []

    def nov_dan(self, teza, visina, starost, spol, aktivnost, datum=None):
        evidenca = Sledilnik(self.id_dneva, teza, visina, starost, spol, aktivnost, datum)
        slovar = evidenca.slovar_dneva()
        self.seznam_dni.append(evidenca)
        self.id_dneva += 1

    def shrani_v_dat(self, datoteka):
        sez = []
        for dan in self.seznam_dni:
            sez.append(dan.slovar_dneva())
        slovar = {
            'ime' : self.ime,
            'geslo' : self.geslo,
            'seznam_dni' : sez,
            'id_dneva' : self.id_dneva
        }
        with open(datoteka, 'w', encoding="utf-8") as dat:
            json.dump(slovar, dat, ensure_ascii=False, indent=6)


    def hrana_po_dnevih(self, teza, visina, starost, spol, aktivnost, datum):
        evidenca = Sledilnik(self.id_dneva, teza, visina, starost, spol, aktivnost, datum)
        dat = evidenca.object_sledilnik(slovar).datum
        hra = evidenca.object_sledilnik(slovar).seznam_hrane
        hrana = []
        for dan in self.seznam_dni:
            hrana.append(dat)
            hrana.append(hra)
        hrana.sort(key=lambda sledilnik: sledilnik.datum)
        return hrana
        
    def vrednosti_po_dnevih(self, teza, visina, starost, spol, aktivnost, datum):
        evidenca = Sledilnik(self.id_dneva, teza, visina, starost, spol, aktivnost, datum)
        vrednosti = []
        for dan in self.seznam_dni:
            vrednosti.append(evidenca.seznam_vrednosti)
        vrednosti.sort(key=lambda sledilnik: sledilnik.datum)
        return vrednosti

    def hrana_danes(self, teza, visina, starost, spol, aktivnost, datum):
        hrana = self.hrana_po_dnevih(teza, visina, starost, spol, aktivnost, datum)
        danes = [datetime.datetime.now().day,
                 datetime.datetime.now().month,
                 datetime.datetime.now().year] 
        danasnje = [
            x for x in hrana if sledilnik.datum == danes 
        ]
        return danasnje

    def vrednosti_danes(self, teza, visina, starost, spol, aktivnost, datum):
        vrednosti = self.vrednosti_po_dnevih(teza, visina, starost, spol, aktivnost, datum)
        danes = [datetime.datetime.now().day,
                 datetime.datetime.now().month,
                 datetime.datetime.now().year] 
        danasnje = [
            x for x in vrednosti if sledilnik.datum == danes
        ]
        return danasnje

    @classmethod
    def object_uporabnik(cls, datoteka):
        with open(datoteka, encoding='utf-8') as dat:
            slovar = json.load(dat)
        ime = slovar.get('ime')
        geslo = slovar.get('geslo')
        id_dneva = slovar.get('id_dneva')

        sez = []
        for dan in slovar.get('seznam_dni'):
            sledilnik = Sledilnik.object_sledilnik(dan)
            sez.append(sledilnik)
        
        uporabnik = cls(ime, geslo)
        uporabnik.id_dneva = id_dneva
        uporabnik.seznam_dni = sez
        return uporabnik


# **********************************************  VSI UPORABNIKI  **************************************************

class VsiUporabniki:
    def __init__(self, mapa):
        self.mapa = mapa
        if not os.path.isdir(mapa):
            os.mkdir(mapa)
        self.uporabniki = self.pokazi_uporabnike(mapa)

    def nov_uporabnik(self, ime, geslo):
        if len(ime) > 0 and len(geslo) > 0 and (ime not in self.uporabniki):
            self.uporabniki[ime] = Uporabnik(ime, geslo)
            return self.uporabniki[ime]
        else:
            return None

    def pokazi_uporabnike(self, mapa):
        uporabniki = {}
        for dat in os.listdir(mapa):
            uporabnik = Uporabnik.object_uporabnik(os.path.join(mapa, dat))
            uporabniki[uporabnik.ime] = uporabnik
        return uporabniki

    def shrani(self, ime):
        self.uporabniki[ime].shrani_v_dat(os.path.join(self.mapa, ime + ".json"))

    def uporabnik_obstaja(self, seznam_imen, ime, geslo):
        # seznam_imen = list(self.uporabniki.keys())         
        if len(seznam_imen) == 0:
            return False
        elif ime == seznam_imen[0] and geslo == self.uporabniki[ime].geslo:
            return True
        else:
            seznam = seznam_imen[1:]
            return self.uporabnik_obstaja(seznam, ime, geslo)

    def tapravi_datum(self, dnevi, datum):
        # uporabnik = self.uporabniki[ime]
        # dnevi = uporabnik.seznam_dni
        if len(dnevi) == 0:
            return False
        elif dnevi[0].datum == datum:
            return True
        else:
            return self.tapravi_datum(dnevi[1:], datum)


# *******************************************  PREGLED DATOTEKE S HRANO  ***********************************************

class Seznam():
    def __init__(self):
        pass
    
    @staticmethod
    def dodaj(hrana, cal, oh, pro, mas):
        with open("C:\\Lucija\\1.letnik fmf\\UVP\\nutrient-tracker\\hrana.txt", 'a', encoding='utf-8') as dat:
            print(hrana + ';' + str(cal) + ';' + str(oh) + ';' + str(pro) + ';' + str(mas), file=dat)
    
    @staticmethod
    def izbrisi(hrana):
        del slovar_za_file[hrana]
        with open("C:\\Lucija\\1.letnik fmf\\UVP\\nutrient-tracker\\hrana.txt", 'w', encoding='utf-8') as dat:
            for stvar in slovar_za_file:
                print(stvar + ';' + str(slovar_za_file.get(stvar)[0]) + ';' + str(slovar_za_file.get(stvar)[1]) + ';' + str(slovar_za_file.get(stvar)[2]) + ';' + str(slovar_za_file.get(stvar)[3]), file=dat)

    @staticmethod
    def odpri_seznam():
        dat = open("C:\\Lucija\\1.letnik fmf\\UVP\\nutrient-tracker\\hrana.txt", 'r', encoding='utf-8')
        print(dat.read())
        dat.close()

    @staticmethod
    def naredi_slovar_hrane():
        slovar = dict()
        with open("C:\\Lucija\\1.letnik fmf\\UVP\\nutrient-tracker\\hrana.txt", encoding="utf-8") as dat:
            for vrstica in dat:
                slovar.update( {seznam(vrstica)[0] : seznam(vrstica)[1:]} )
        return slovar