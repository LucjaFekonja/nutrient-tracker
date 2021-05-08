% rebase('osnova.tpl')

<a class='alignright' href="/odjava/" style='color:white'>Odjava</a>
<h1><div class='naslov'>Dodaj na seznam</div></h1>

<div class='container-small'>
    <form action='/{{ime_uporabnika}}/{{datum}}/dodaj_na_seznam/' method="POST">
        <label for="hrana"><b>Hrana: </b></label>
        <input type="text2" name="hrana" required>
        <br><br>
        <p style="margin:auto"><label for="cal"><b>Kalorije: </b></label>
        <input type="number" step="0.01" name="cal" required> g / 100 g</p>
        <br>
        <p style="margin:auto"><label for="oh"><b>Ogljikovi hidrati: </b></label>
        <input type="number" step="0.01" name="oh" required> g / 100 g</p>
        <br>
        <p style="margin:auto"><label for="pro"><b>Proteini: </b></label>
        <input type="number" step="0.01" name="pro" required> g / 100 g</p>
        <br>
        <p style="margin:auto"><label for="mas"><b>Maščobe: </b></label>
        <input type="number" step="0.01" name="mas" required> g / 100 g</p>

        <br>
        <button class='button button1' type="submit">Pošlji</button>
    </form>
</div>

<table id='vrednosti-tabela'>
    <tr>
        <th>Hrana</th>
        <th>Kalorije</th>
        <th>Ogljikovi hidrati</th>
        <th>Proteini</th>
        <th>Maščobe</th>
    </tr>

    % for hrana in slovar.keys():
    <tr>
        <td style='font-weight: bold;'>{{hrana}}</td>
        <td style="width: 17%; text-align: center;">{{slovar.get(hrana)[0]}}</td>
        <td style="width: 17%; text-align: center">{{slovar.get(hrana)[1]}}</td>
        <td style="width: 17%; text-align: center">{{slovar.get(hrana)[2]}}</td>
        <td style="width: 17%; text-align: center">{{slovar.get(hrana)[3].strip('n\n')}}</td>
    </tr>
    % end
</table>