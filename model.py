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
            return int(round(self.bmr_na_aktivnost(), 0)) + 500
        if 18.5 <= self.bmi < 25:
            return int(round(self.bmr_na_aktivnost(), 0))
        if self.bmi >= 25:
            return int(round(self.bmr_na_aktivnost(), 0)) - 500
    
    def priporocene(self):
        priporocene_mascobe = self.priporocene_cal() * 25 / 400
        priporoceni_ogljikovi = self.priporocene_cal() * 50 / 400
        priporoceni_proteini = self.priporocene_cal() * 25 / 400
        return (int(priporoceni_ogljikovi), int(priporoceni_proteini), int(priporocene_mascobe))


# *******************************************  VODENJE EVIDENCE  ***********************************************

def seznam(niz):
    sez1 = niz.split(';')
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
        self.cal = 0
        self.mascobe = 0
        self.ogljikovi = 0
        self.proteini = 0   
        self.vse_cal = self.priporocene_cal()
        self.vsi_ogljikovi = self.priporocene()[0]
        self.vsi_proteini = self.priporocene()[1]
        self.vse_mascobe = self.priporocene()[2]
        self.seznam_hrane = dict()
        self.seznam_vrednosti = dict()
        self.id = id
        self.datum = datum


    def dodaj(self, hrana, gram):
        """
        Funkcija k porabljenim doda vrednosti iz datoteke hrana.txt,
        od vseh priporočenih odšteje iste količine in
        doda navedeno hrano in grame na seznam_hrane.
        """
        vrednosti = slovar[hrana]
        self.cal += float(vrednosti[0]) * float(gram) / 100
        self.ogljikovi += float(vrednosti[1]) * float(gram) / 100
        self.proteini += float(vrednosti[2]) * float(gram) / 100
        self.mascobe += float(vrednosti[3]) * float(gram) / 100

        self.vse_cal -= float(vrednosti[0]) * float(gram) / 100
        self.vsi_ogljikovi -= float(vrednosti[1]) * float(gram) / 100
        self.vsi_proteini -= float(vrednosti[2]) * float(gram) / 100
        self.vse_mascobe -= float(vrednosti[3]) * float(gram) / 100
        sez1 = (self.cal, self.ogljikovi, self.proteini, self.mascobe, 
                self.vse_cal, self.vsi_ogljikovi, self.vsi_proteini, self.vse_mascobe)
        
        self.dodaj_na_seznam_hrane(hrana, float(gram))

        sez2 = []
        for element in sez1:
            sez2 += [round(element, 1)]
        return sez2


    def izbrisi(self, hrana):
        """
        Funkcija od porabljenih odvzame vrednosti iz datoteke hrana.txt,
        k priporočenim doda iste količine in
        izbriše navedeno hrano in grame iz seznam_hrane.
        """
        if hrana in self.pokazi_seznam_hrane():
            vrednosti = slovar[hrana]
            kolicina = self.pokazi_seznam_hrane()[hrana]
            self.cal -= float(vrednosti[0]) * kolicina / 100
            self.ogljikovi -= float(vrednosti[1]) * kolicina / 100
            self.proteini -= float(vrednosti[2]) * kolicina / 100
            self.mascobe -= float(vrednosti[3]) * kolicina / 100

            self.vse_cal += float(vrednosti[0]) * kolicina / 100
            self.vsi_ogljikovi += float(vrednosti[1]) * kolicina / 100
            self.vsi_proteini += float(vrednosti[2]) * kolicina / 100
            self.vse_mascobe += float(vrednosti[3]) * kolicina / 100
            sez1 = (self.cal, self.ogljikovi, self.proteini, self.mascobe, 
                    self.vse_cal, self.vsi_ogljikovi, self.vsi_proteini, self.vse_mascobe)
            
            self.izbrisi_iz_seznama_hrane(hrana)

            sez2 = []
            for element in sez1:
                sez2 += [round(element, 1)]
            return sez2
        else:
            print('Navedene hrane niste dodali.')

    # ------------  Funkcije uporabljene zgoraj  ------------
    def dodaj_na_seznam_hrane(self, hrana, gram):
        return self.seznam_hrane.update( {hrana : gram} )

    def izbrisi_iz_seznama_hrane(self, hrana):
        del self.seznam_hrane[hrana]  

    def pokazi_seznam_hrane(self):
        return self.seznam_hrane

    # ------------  Funkcije uporabljene v naprej  ------------
    def porabljeno(self):
        return [self.cal, self.ogljikovi, self.proteini, self.mascobe]

    def preostalo(self):
        return [self.vse_cal, self.vsi_ogljikovi, self.vsi_proteini, self.vse_mascobe]

    # Naredimo class object, na katerega se bomo sklicevali v drugih razredih
    def slovar_vrednosti(self):
        slovar = {
            'datum' : self.datum,
            'cal' : self.porabljeno()[0],
            'oh' : self.porabljeno()[1],
            'pro' : self.porabljeno()[2],
            'mas' : self.porabljeno()[3],
            'vse_cal' : self.preostalo()[0],
            'vse_oh' : self.preostalo()[1],
            'vse_pro' : self.preostalo()[2],
            'vse_mas' : self.preostalo()[3]
        }
        return slovar
    
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
            'seznam_vrednosti' : self.slovar_vrednosti(),
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
        self.id_dneva = 1
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
        danes = [datetime.datetime.now().year, 
                 datetime.datetime.now().month,
                 datetime.datetime.now().day]
        danasnje = [
            x for x in hrana if sledilnik.datum == danes 
        ]
        return danasnje

    def vrednosti_danes(self, teza, visina, starost, spol, aktivnost, datum):
        vrednosti = self.vrednosti_po_dnevih(teza, visina, starost, spol, aktivnost, datum)
        danes = [datetime.datetime.now().year, 
                 datetime.datetime.now().month,
                 datetime.datetime.now().day]
        danasnje = [
            x for x in vrednosti if sledilnik.datum == danes
        ]
        return danasnje

    @classmethod
    def object_uporabnik(cls, datoteka):
        with open(datoteka, encoding='utf-8') as dat:
            slovar = json.load(dat)
        ime = slovar['ime']
        geslo = slovar['geslo']
        id_dneva = slovar['id_dneva']

        sez = []
        for dan in slovar['seznam_dni']:
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
            uporabnik = Uporabnik.object_uporabnik(
                os.path.join(mapa, dat))
            uporabniki[uporabnik.ime] = uporabnik
        return uporabniki

    def shrani_uporabnika(self, ime):
        self.uporabniki[ime].shrani_v_dat(os.path.join(self.mapa, ime + ".json"))