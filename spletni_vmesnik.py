import bottle
import model
import datetime

with open('sifra.txt') as d:
    SKRIVNOST = d.read()

seznam_uporabnikov = model.VsiUporabniki('uporabniki')
slovar_hrane = model.Seznam('hrana.txt')

#######################################  LOGIN PAGE   #######################################
@bottle.get('/')
def index():
    return bottle.template('login.tpl')

@bottle.post('/prijava/')
def login():
    ime = bottle.request.forms.getunicode('ime')
    geslo = bottle.request.forms.getunicode('geslo')
    datum = str(datetime.date.today())
    datum_list = datum_kot_seznam(datum)

    if seznam_uporabnikov.uporabnik_obstaja(list(seznam_uporabnikov.uporabniki.keys()), ime, geslo) == False:
        # Preverimo, če uporabnik sploh obstaja. Če ne obstaja... 
        return bottle.redirect('/')
    else:
        bottle.response.set_cookie('ime', ime, secret=SKRIVNOST, path='/')
        uporabnik = seznam_uporabnikov.uporabniki[ime]
        dnevi = uporabnik.seznam_dni
        if seznam_uporabnikov.tapravi_datum(dnevi, datum_list) == False:
            # Če obstaja, preverimo, če ima vnesene kakšne vrednosti za danes. 
            # Če nima, naredimo nov dan. 
            dan = uporabnik.seznam_dni[-1]
            uporabnik.nov_dan(dan.teza,
                              dan.visina,
                              dan.starost,
                              dan.spol,
                              dan.aktivnost,
                              datum_list
                              )
            seznam_uporabnikov.shrani(ime)
            return bottle.redirect('/front-page/{}'.format(datum))
        else:
            # Če ima, vrnemo stran z že vnešenimi podatki. 
            return bottle.redirect('/front-page/{}'.format(datum))


#######################################  SIGN IN PAGE   #######################################

@bottle.get('/vpis/')
def sign_in():
    return bottle.template('views/sign_in.tpl')

@bottle.post('/vpis/')
def sign_in():
    ime = bottle.request.forms.getunicode('ime')
    geslo = bottle.request.forms.getunicode('geslo')
    teza = float(bottle.request.forms.getunicode('teza'))
    visina = float(bottle.request.forms.getunicode('visina'))
    starost = float(bottle.request.forms.getunicode('starost'))
    spol = str(bottle.request.forms.getunicode('spol'))
    aktivnost = str(bottle.request.forms.getunicode('aktivnost'))
    datum_str = datetime.date.today()
    datum = datum_kot_seznam(str(datum_str))

    if seznam_uporabnikov.uporabnik_obstaja(list(seznam_uporabnikov.uporabniki.keys()), ime, geslo) == False:
        seznam_uporabnikov.nov_uporabnik(ime, geslo)                         # ustvarimo novega uporabnika iz podatkov
        uporabnik = seznam_uporabnikov.uporabniki[ime]                       # dostopamo do uporabnika
        uporabnik.nov_dan(teza, visina, starost, spol, aktivnost, datum)     # dodamo nov dan na seznam_dni
        seznam_uporabnikov.shrani(ime)                                       # shranimo v json v mapi 'uporabniki'
        bottle.response.set_cookie('ime', ime, secret=SKRIVNOST, path='/')
        return bottle.redirect('/front-page/{}'.format(datum_str))
    else:
        return bottle.redirect('/vpis/')


#######################################  FRONT PAGE   #######################################

@bottle.get('/front-page/<datum>')
def front_page(datum):
    datum_list = datum_kot_seznam(datum)
    ime = str(bottle.request.get_cookie('ime', secret=SKRIVNOST))
    seznam_vrednosti = dnevni_seznam_vrednosti(datum_list, ime)        # Ti dve funkciji sta na koncu datoteke
    slovar_hrane = dnevni_slovar_hrane(datum_list, ime)
    datum_str = '. '.join([str(x) for x in datum.split('-')[::-1]])

    return bottle.template('views/front-page.tpl', ime=ime,
                                                   datum=datum,
                                                   seznam_vrednosti=seznam_vrednosti,
                                                   slovar_hrane=slovar_hrane,
                                                   datum_str=datum_str)

@bottle.post('/fp-izberi-dan/')
def front_page_dneva(): 
    ime = str(bottle.request.get_cookie('ime', secret=SKRIVNOST))
    uporabnik = seznam_uporabnikov.uporabniki.get(ime)
    dnevi = uporabnik.seznam_dni
    datum_str  = bottle.request.forms.getunicode('datum')
    datum = datum_kot_seznam(datum_str)

    if seznam_uporabnikov.tapravi_datum(dnevi, datum) == False:
        dan = uporabnik.seznam_dni[-1]
        uporabnik.nov_dan(dan.teza,
                          dan.visina,
                          dan.starost,
                          dan.spol,
                          dan.aktivnost,
                          datum
                          )
        seznam_uporabnikov.shrani(ime)
        return bottle.redirect('/front-page/{}'.format(datum_str))
    else:
        return bottle.redirect('/front-page/{}'.format(datum_str))
    

@bottle.post('/fp-izbrisi/<datum>')
def izbrisi(datum):
    ime = bottle.request.get_cookie('ime', secret=SKRIVNOST)
    
    uporabnik = seznam_uporabnikov.uporabniki.get(ime)
    seznam_dni = uporabnik.seznam_dni
    
    hrana = bottle.request.forms.getunicode('hrana')
    datum_list = datum_kot_seznam(datum)
    dan_z_datumom(seznam_dni, datum_list).izbrisi(hrana)
    seznam_uporabnikov.shrani(ime)
    return bottle.redirect('/front-page/{}'.format(datum))    


@bottle.post('/fp-nazaj/<datum>')
def na_front_page(datum):
    return bottle.redirect('/front-page/{}'.format(datum))
    

##########################################   SPREMENI PODATKE   ##########################################

@bottle.post('/fp-spremeni_podatke/<datum>')
def gumb_spremeni_podatke(datum):
    return bottle.redirect('/spremeni_podatke/{}'.format(datum))

@bottle.get('/spremeni_podatke/<datum>')
def spremeni(datum):
    ime = bottle.request.get_cookie('ime', secret=SKRIVNOST)
    uporabnik = seznam_uporabnikov.uporabniki.get(ime)
    dan = dan_z_datumom(uporabnik.seznam_dni, datum_kot_seznam(datum))
    
    return bottle.template('views/spremeni.tpl', datum=datum,
                                                 dan=dan)

@bottle.post('/spremeni_podatke/<datum>')
def spremeni(datum):
    ime = bottle.request.get_cookie('ime', secret=SKRIVNOST)
    uporabnik = seznam_uporabnikov.uporabniki.get(ime)
    dan = dan_z_datumom(uporabnik.seznam_dni, datum_kot_seznam(datum))

    dan.teza = float(bottle.request.forms.getunicode('teza'))
    dan.visina = float(bottle.request.forms.getunicode('visina'))
    dan.starost = float(bottle.request.forms.getunicode('starost'))
    dan.spol = str(bottle.request.forms.getunicode('spol'))
    dan.aktivnost = str(bottle.request.forms.getunicode('aktivnost'))

    vrednosti = dan.seznam_vrednosti

#   sez1 = ['vse_oh', ...]
#   for x, i in sez1, range(0, 3):
#       vrednosti[x] = dan.priporocene()[i]

    vrednosti["vse_cal"] = dan.priporocene_cal()
    vrednosti["vsi_oh"] = dan.priporocene()[0]
    vrednosti["vsi_pro"] = dan.priporocene()[1]
    vrednosti["vse_mas"] = dan.priporocene()[2]
    vrednosti["preostale_cal"] = round(dan.priporocene_cal() - vrednosti['porabljene_cal'], 1)
    vrednosti["preostali_oh"] = round(dan.priporocene()[0] - vrednosti['porabljeni_oh'], 1)
    vrednosti["preostali_pro"] = round(dan.priporocene()[1] - vrednosti['porabljeni_pro'], 1)
    vrednosti["preostale_mas"] = round(dan.priporocene()[2] - vrednosti['porabljene_mas'], 1)

    seznam_uporabnikov.shrani(ime)
    return bottle.redirect('/front-page/{}'.format(datum)) 

##########################################   DODAJ   ##########################################

@bottle.post('/fp-dodaj/<datum>')
def gumb_dodaj(datum):
    return bottle.redirect('/front-page/{}/dodaj'.format(datum))

@bottle.get('/front-page/<datum>/dodaj')
def dodaj(datum):
    slovar = slovar_hrane.naredi_slovar_hrane()
    return bottle.template('views/dodaj.tpl', datum=datum,
                                              slovar=slovar)

@bottle.post('/dodaj/<datum>/')
def dodaj(datum):
    ime = bottle.request.get_cookie('ime', secret=SKRIVNOST)
    uporabnik = seznam_uporabnikov.uporabniki.get(ime)
    seznam_dni = uporabnik.seznam_dni

    hrana = bottle.request.forms.getunicode('hrana').lower()
    gram = float(bottle.request.forms.getunicode('gram'))

    datum_list = datum_kot_seznam(datum)
    dan_z_datumom(seznam_dni, datum_list).dodaj(hrana, gram)
    seznam_uporabnikov.shrani(ime)
    return bottle.redirect('/front-page/{}'.format(datum))


#######################################  DODAJ NA SEZNAM   #######################################

@bottle.post('/odpri_na_seznam/<datum>')
def gumb_dodaj_na_seznam(datum):
    return bottle.redirect('/dodaj_na_seznam/{}'.format(datum))

@bottle.get('/dodaj_na_seznam/<datum>')
def dodaj_na_seznam(datum):
    ime = bottle.request.get_cookie('ime', secret=SKRIVNOST)
    slovar = slovar_hrane.naredi_slovar_hrane()
    return bottle.template('views/dodaj_na_seznam.tpl', ime=ime,
                                                        datum=datum,
                                                        slovar=slovar)

@bottle.post('/dodaj_na_seznam/<datum>/')
def dodaj_na_seznam(datum):
    hrana = bottle.request.forms.getunicode('hrana').lower()
    cal = bottle.request.forms.getunicode('cal').replace(',', '.')
    oh = bottle.request.forms.getunicode('oh').replace(',', '.')
    pro = bottle.request.forms.getunicode('pro').replace(',', '.')
    mas = bottle.request.forms.getunicode('mas').replace(',', '.')

    slovar_hrane.dodaj(hrana, cal, oh, pro, mas)
    return bottle.redirect('/dodaj_na_seznam/{}'.format(datum))

@bottle.post('/izbrisi-iz-seznama/<datum>/')
def izbrisi_iz_seznama(datum):
    hrana = bottle.request.forms.getunicode('hrana')
    slovar_hrane.izbrisi(hrana)
    return bottle.redirect('/dodaj_na_seznam/{}'.format(datum))


############################################  ODJAVA   ############################################

@bottle.post('/odjava/')
def sign_out():
    ime = bottle.request.get_cookie('ime', secret=SKRIVNOST)
    bottle.response.delete_cookie('ime', ime, secret=SKRIVNOST, path='/')
    return bottle.redirect('/')


#####################################  UPORABLJENE FUNKCIJE   #####################################
def dnevni_seznam_vrednosti(datum, ime):
    uporabnik = seznam_uporabnikov.uporabniki[ime]
    dan = dan_z_datumom(uporabnik.seznam_dni, datum)
    return dan.seznam_vrednosti 

def dnevni_slovar_hrane(datum, ime):
    uporabnik = seznam_uporabnikov.uporabniki[ime]
    dan = dan_z_datumom(uporabnik.seznam_dni, datum)
    return dan.seznam_hrane

def dan_z_datumom(seznam_dni, datum):
    # seznam_dni = seznam_uporabnikov.uporabniki['ime'].seznam_dni
    for sez in seznam_dni:
        if sez.datum == datum:
            return sez

def datum_kot_seznam(niz):
    return [int(x) for x in niz.split('-')]


###############################################     ###############################################

bottle.run(reloader=True, debug=True)