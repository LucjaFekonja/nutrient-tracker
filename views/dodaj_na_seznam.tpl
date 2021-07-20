% rebase('osnova.tpl')

<form class='alignleft' action="/fp-nazaj/{{datum}}" method="POST" style='color:white'>
    <button class='button button4' type="submit" >Nazaj</button>
</form>

<form class='alignright' action="/odjava/" method="POST" style='color:white'>
    <button class='button button4' type="submit" >Odjava</button>
</form>

<h1><div class='naslov'>Dodaj na seznam</div></h1>

<div class='container-small'>
    <form action='/dodaj_na_seznam/{{datum}}/' method="POST">
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
        <td style="width: 17%; text-align: center">{{slovar.get(hrana)[3]}}</td>
        <td style="text-align: center;">
            <form action="/izbrisi-iz-seznama/{{datum}}/" method="POST">
                <button class="button-izbrisi" name="hrana" value="{{hrana}}" type="submit">Izbriši</button>
            </form>
        </td>
    </tr>
    % end
</table>