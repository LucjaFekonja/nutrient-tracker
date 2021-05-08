% rebase('osnova.tpl')

<a href="/odjava/" class='alignright' style='color:white' >Odjava</a>

<form class='alignleft' action='/fp-izberi-dan/' method="POST">
    <label for="datum">Datum: </label>
    <input type="date" id="datum" name='datum' required> 
    <button class='button button4' type="submit" >Pošlji</button>
</form>

<h1><div class='naslov-fp'>{{datum_str}}<div></h1>

<div class='container-small' style="border-color: #04AA6D;">
% include('progress.html', oznaka='Kalorije', 
%                          dolzina=seznam_vrednosti.get("porabljene_cal") / seznam_vrednosti.get("vse_cal") * 100)

<br>
% include('progress.html', oznaka='Ogljikovi hidrati', 
%                          dolzina=seznam_vrednosti.get("porabljeni_oh") / seznam_vrednosti.get("vsi_oh") * 100)
<br>
% include('progress.html', oznaka='Proteini', 
%                          dolzina=seznam_vrednosti.get("porabljeni_pro") / seznam_vrednosti.get("vsi_pro") * 100)
<br>
% include('progress.html', oznaka='Maščobe', 
%                          dolzina=seznam_vrednosti.get("porabljene_mas") / seznam_vrednosti.get("vse_mas") * 100)
</div>
<br><br>
<table id='hrana-tabela'>
    <tr>
        <th>Hrana</th>
        <th>Količina</th>
    </tr>

    % for hrana in slovar_hrane.keys():
    <tr>
        <td>{{hrana}}</td>
        <td style="width: 30%;">{{slovar_hrane.get(hrana)}} g</td>
    </tr>
    % end
</table>
<br>

<form action='/fp-dodaj/{{ime_uporabnika}}/{{datum}}' method="POST">
    <button class='button button2' type="submit">Dodaj</button>
</form>
