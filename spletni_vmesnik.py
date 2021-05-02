import bottle
import model
import datetime
import json

seznam_uporabnikov = model.VsiUporabniki('uporabniki')

@bottle.get('/')
def index():
    return bottle.template('login.tpl')

@bottle.post('/prijava/')
def login():
    ime = bottle.request.forms.getunicode('ime')
    geslo = bottle.request.forms.getunicode('geslo')
    uporabnik = seznam_uporabnikov.uporabniki[ime]
    id_dneva = uporabnik.id_dneva

    if geslo == uporabnik.geslo:
        return bottle.redirect('/front-page/{}/{}'.format(ime, id_dneva))
    else:
        return bottle.redirect('/')


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
    datum = datetime.date.today()
 
    seznam_uporabnikov.nov_uporabnik(ime, geslo)
    seznam_uporabnikov.shrani(ime)    

    uporabnik = seznam_uporabnikov.uporabniki[ime]
    uporabnik.nov_dan(teza, visina, starost, spol, aktivnost, datum)
    id = uporabnik.id_dneva

    if seznam_uporabnikov.preveri_ime_geslo(ime, geslo) is True:
        return bottle.redirect('/front-page/{}/{}'.format(ime, id))
    else:
        bottle.redirect('/vpis/')


@bottle.get('/front-page/<ime_uporabnika>/<id_dneva:int>')
def front_page(ime_uporabnika, id_dneva):
    return bottle.template('views/front-page.tpl', ime_uporabnika=ime_uporabnika, id_dneva=id_dneva)


bottle.run(reloader=True, debug=True)