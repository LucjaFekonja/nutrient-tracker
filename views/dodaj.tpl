%rebase('osnova.tpl')

<form class='alignleft' action="/fp-nazaj/{{ime_uporabnika}}/{{datum}}" method="POST" style='color:white'>
    <button class='button button4' type="submit" >Nazaj</button>
</form>

<form class='alignright' action="/odjava/" method="POST" style='color:white'>
    <button class='button button4' type="submit" >Odjava</button>
</form>
<h1><div class='naslov-fp'>Vpiši hrano<div></h1>

<div class='container-small'>
    <form action='/dodaj/{{ime_uporabnika}}/{{datum}}/' method="POST">
        <table style='width:50%'>
            <tr>
              <td width='30%'><b>Hrana:</b></td>
              <td width='70%'>
                  <select name="hrana">
                  % for hrana in slovar.keys():
                  <option value="{{hrana}}">{{hrana}}</option>
                  %end
                </select>
              </td>
            </tr>
          </table>

        <p><label for="gram"><b>Količina: </b></label>
        <input type="number" name="gram" required> g</p>
    
        <br>
        <button class='button button1' type="submit">Dodaj</button>
    </form>
</div>

<p style='font-size:12px; color:indigo; text-align:center'>Željene jedi ni na seznamu hrane? Dodajte jo s klikom na spodnji gumb.</p>
<form action='/odpri_na_seznam/' method="POST">
    <button class='button button3' style='margin-top:0.5cm;' type="submit">Dodaj v seznam</button>
</form>
