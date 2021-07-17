% rebase('osnova.tpl')

<form class='alignright' action="/odjava/" method="POST" style='color:white'>
    <button class='button button4' type="submit" >Odjava</button>
</form>

<form class='alignleft' action='/fp-izberi-dan/{{ime_uporabnika}}' method="POST">
    <label for="datum">Datum: </label>
    <input type="date" id="datum" name='datum' required> 
    <button class='button button4' type="submit" >Pošlji</button>
</form>

<h1><div class='naslov-fp'>{{datum_str}}<div></h1>

<form action='/fp-spremeni_podatke/{{ime_uporabnika}}/{{datum}}' method="POST">
    <button class='button button2' style='background-color:gray' type="submit">Spremeni osebne podatke</button>
</form>

<br><br><br><br><br>
<div class='container-small' style="border-color: #04AA6D;">
% include('progress.html', oznaka='Kalorije', 
%                          porabljene=seznam_vrednosti.get("porabljene_cal"),
%                          vse=seznam_vrednosti.get("vse_cal"),
%                          dolzina=seznam_vrednosti.get("porabljene_cal") / seznam_vrednosti.get("vse_cal") * 100,)
<br>
% include('progress.html', oznaka='Ogljikovi hidrati', 
%                          porabljene=seznam_vrednosti.get("porabljeni_oh"),
%                          vse=seznam_vrednosti.get("vsi_oh"),
%                          dolzina=seznam_vrednosti.get("porabljeni_oh") / seznam_vrednosti.get("vsi_oh") * 100)
<br>
% include('progress.html', oznaka='Proteini', 
%                          porabljene=seznam_vrednosti.get("porabljeni_pro"),
%                          vse=seznam_vrednosti.get("vsi_pro"),
%                          dolzina=seznam_vrednosti.get("porabljeni_pro") / seznam_vrednosti.get("vsi_pro") * 100)
<br>
% include('progress.html', oznaka='Maščobe', 
%                          porabljene=seznam_vrednosti.get("porabljene_mas"),
%                          vse=seznam_vrednosti.get("vse_mas"),
%                          dolzina=seznam_vrednosti.get("porabljene_mas") / seznam_vrednosti.get("vse_mas") * 100)
</div>
<br><br>
<table id='hrana-tabela'>
    <tr>
        <th>Hrana</th>
        <th>Količina</th>
        <th></th>
    </tr>

    % for hrana in slovar_hrane.keys():
    <tr>
        <td>{{hrana}}</td>
        <td style="width: 30%;">{{slovar_hrane.get(hrana)}} g</td>
        <td style="text-align: center;">
            <form action="/fp-izbrisi/{{ime_uporabnika}}/{{datum}}" method="POST">
                <button class="button-izbrisi" name="hrana" value="{{hrana}}" type="submit">Izbriši</button>
            </form>
        </td>
    </tr>
    % end
</table>
<br>

<form action='/fp-dodaj/{{ime_uporabnika}}/{{datum}}' method="POST">
    <button class='button button2' type="submit">Dodaj</button>
</form>
