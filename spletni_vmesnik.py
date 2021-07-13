import bottle
import model
import datetime

SKRIVNOST = 'banana'
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
    datum_list = [int(x) for x in datum.split('-')]

    if seznam_uporabnikov.uporabnik_obstaja(list(seznam_uporabnikov.uporabniki.keys()), ime, geslo) == False:
        # Preverimo, če uporabnik sploh obstaja. Če ne obstaja... 
        return bottle.redirect('/')
    else:
        uporabnik = seznam_uporabnikov.uporabniki[ime]
        dnevi = uporabnik.seznam_dni
        if seznam_uporabnikov.tapravi_datum(dnevi, [int(x) for x in datum.split('-')]) == False:
            # Če obstaja, preverimo, če ima vnesene kakšne vrednosti za danes. 
            # Če nima, naredimo nov dan. 
            dan = uporabnik.seznam_dni[-1]
            vrednosti_zadnjega = {'teza' : dan.teza,
                                  'visina' : dan.visina,
                                  'starost' : dan.starost,
                                  'spol' : dan.spol,
                                  'aktivnost' : dan.aktivnost                             
                                  }
            uporabnik.nov_dan(dan.teza,
                              dan.visina,
                              dan.starost,
                              dan.spol,
                              dan.aktivnost,
                              datum_list
                              )
            seznam_uporabnikov.shrani(ime)
            bottle.response.set_cookie('ime', '{}'.format(ime), secret=SKRIVNOST, path='/')
            return bottle.redirect('/front-page/{}/{}'.format(ime, datum))
        else:
            # Če ima, vrnemo stran z že vnešenimi podatki. 
            return bottle.redirect('/front-page/{}/{}'.format(ime, datum))


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
    datum = [int(x) for x in str(datum_str).split('-')]

    seznam_uporabnikov.nov_uporabnik(ime, geslo)                         # ustvarimo novega uporabnika iz podatkov
    uporabnik = seznam_uporabnikov.uporabniki[ime]                       # dostopamo do uporabnika
    uporabnik.nov_dan(teza, visina, starost, spol, aktivnost, datum)     # dodamo nov dan na seznam_dni
    seznam_uporabnikov.shrani(ime)                                       # shranimo v json v mapi 'uporabniki'

    return bottle.redirect('/front-page/{}/{}'.format(ime, datum_str))


#######################################  FRONT PAGE   #######################################

@bottle.get('/front-page/<ime_uporabnika>/<datum>')
def front_page(ime_uporabnika, datum):
    datum_list = [int(x) for x in datum.split('-')]
    seznam_vrednosti = dnevni_seznam_vrednosti(datum_list, ime_uporabnika)
    slovar_hrane = dnevni_slovar_hrane(datum_list, ime_uporabnika)
    datum_str = '. '.join([str(x) for x in datum.split('-')[::-1]])

    return bottle.template('views/front-page.tpl', ime_uporabnika=ime_uporabnika,
                                                   datum=datum,
                                                   seznam_vrednosti=seznam_vrednosti,
                                                   slovar_hrane=slovar_hrane,
                                                   datum_str=datum_str)

@bottle.post('/fp-izbrisi/<ime_uporabnika>/<datum>')
def izbrisi(ime_uporabnika, datum):
    ime = bottle.request.get_cookie('ime', secret=SKRIVNOST)
    uporabnik = seznam_uporabnikov.uporabniki.get(ime_uporabnika)
    seznam_dni = uporabnik.seznam_dni
    
    hrana = bottle.request.forms.getunicode('hrana')
    print(hrana)
    datum_list = [int(x) for x in datum.split('-')]
    dan_z_datumom(seznam_dni, datum_list).izbrisi(hrana)
    seznam_uporabnikov.shrani(ime_uporabnika)
    return bottle.redirect('/front-page/{}/{}'.format(ime_uporabnika, datum))


@bottle.post('/fp-izberi-dan/<ime_uporabnika>')
def front_page_dneva(ime_uporabnika): 
    ime = str(bottle.request.get_cookie('ime', secret=SKRIVNOST))
    uporabnik = seznam_uporabnikov.uporabniki.get(ime_uporabnika)
    dnevi = uporabnik.seznam_dni
    datum_str  = bottle.request.forms.getunicode('datum')
    datum = [int(x) for x in datum_str.split('-')]

    if seznam_uporabnikov.tapravi_datum(dnevi, datum) == False:
        dan = uporabnik.seznam_dni[-1]
        vrednosti_zadnjega = {'teza' : dan.teza,
                              'visina' : dan.visina,
                              'starost' : dan.starost,
                              'spol' : dan.spol,
                              'aktivnost' : dan.aktivnost                             
                              }
        uporabnik.nov_dan(dan.teza,
                          dan.visina,
                          dan.starost,
                          dan.spol,
                          dan.aktivnost,
                          datum
                          )
        seznam_uporabnikov.shrani(ime_uporabnika)
        return bottle.redirect('/front-page/{}/{}'.format(ime_uporabnika, datum_str))
    else:
        return bottle.redirect('/front-page/{}/{}'.format(ime_uporabnika, datum_str))
    
    
##########################################   DODAJ   ##########################################

@bottle.post('/fp-dodaj/<ime_uporabnika>/<datum>')
def gumb_dodaj(ime_uporabnika, datum):
    ime = bottle.request.get_cookie('ime', secret=SKRIVNOST)
    return bottle.redirect('/front-page/{}/{}/dodaj'.format(ime_uporabnika, datum))

@bottle.get('/front-page/<ime_uporabnika>/<datum>/dodaj')
def dodaj(ime_uporabnika, datum):
    return bottle.template('views/dodaj.tpl', ime_uporabnika=ime_uporabnika,
                                              datum=datum)

@bottle.post('/dodaj/<ime_uporabnika>/<datum>/')
def dodaj(ime_uporabnika, datum):
    ime = bottle.request.get_cookie('ime', secret=SKRIVNOST)
    uporabnik = seznam_uporabnikov.uporabniki.get(ime_uporabnika)
    seznam_dni = uporabnik.seznam_dni

    hrana = bottle.request.forms.getunicode('hrana').lower()
    gram = float(bottle.request.forms.getunicode('gram'))

    if hrana not in list(slovar_hrane.naredi_slovar_hrane().keys()):
        return bottle.redirect('/front-page/{}/{}/ni'.format(ime_uporabnika, datum))
    else:
        datum_list = [int(x) for x in datum.split('-')]
        dan_z_datumom(seznam_dni, datum_list).dodaj(hrana, gram)
        seznam_uporabnikov.shrani(ime_uporabnika)
        return bottle.redirect('/front-page/{}/{}'.format(ime_uporabnika, datum))


@bottle.get('/front-page/<ime_uporabnika>/<datum>/ni')
def dodaj_ne_gre(ime_uporabnika, datum):
    return bottle.template('views/dodaj_ne_gre.tpl', ime_uporabnika=ime_uporabnika,
                                                     datum=datum)


#######################################  DODAJ NA SEZNAM   #######################################

@bottle.post('/<ime_uporabnika>/<datum>/odpri_na_seznam/')
def gumb_dodaj_na_seznam(ime_uporabnika, datum):
    return bottle.redirect('/{}/{}/dodaj_na_seznam'.format(ime_uporabnika, datum))

@bottle.get('/<ime_uporabnika>/<datum>/dodaj_na_seznam')
def dodaj_na_seznam(ime_uporabnika, datum):
    slovar = slovar_hrane.naredi_slovar_hrane()
    return bottle.template('views/dodaj_na_seznam.tpl', ime_uporabnika=ime_uporabnika,
                                                        datum=datum,
                                                        slovar=slovar)

@bottle.post('/<ime_uporabnika>/<datum>/dodaj_na_seznam/')
def dodaj_na_seznam(ime_uporabnika, datum):
    hrana = bottle.request.forms.getunicode('hrana').lower()
    cal = bottle.request.forms.getunicode('cal').replace(',', '.')
    oh = bottle.request.forms.getunicode('oh').replace(',', '.')
    pro = bottle.request.forms.getunicode('pro').replace(',', '.')
    mas = bottle.request.forms.getunicode('mas').replace(',', '.')

    slovar_hrane.dodaj(hrana, cal, oh, pro, mas)
    return bottle.redirect('/front-page/{}/{}'.format(ime_uporabnika, datum))

@bottle.post('/<ime_uporabnika>/<datum>/izbrisi-iz-seznama/')
def izbrisi_iz_seznama(ime_uporabnika, datum):
    hrana = bottle.request.forms.getunicode('hrana')
    slovar_hrane.izbrisi(hrana)
    return bottle.redirect('/front-page/{}/{}'.format(ime_uporabnika, datum))


############################################  ODJAVA   ############################################

@bottle.get('/odjava/')
def sign_in():
    return bottle.template('views/login.tpl')


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
    # seznam_dni = seznam_uporabnikov.uporabniki['Lucija'].seznam_dni
    for sez in seznam_dni:
        if sez.datum == datum:
            return sez


###############################################     ###############################################

bottle.run(reloader=True, debug=True)