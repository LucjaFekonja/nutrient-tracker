%rebase('osnova.tpl')

<form class='alignright' action="/odjava/" method="POST" style='color:white'>
    <button class='button button4' type="submit" >Odjava</button>
</form>
<h1><div class='naslov-fp'>Vpiši hrano<div></h1>

<div class='container-small'>
    <form action='/dodaj/{{ime_uporabnika}}/{{datum}}/' method="POST">
        <label for="hrana"><b>Hrana: </b></label>
        <input type="text2" name="hrana" required>

        <p><label for="gram"><b>Količina: </b></label>
        <input type="number" name="gram" required> g</p>
    
        <br>
        <button class='button button1' type="submit">Dodaj</button>
    </form>
</div>

<form action='/odpri_na_seznam/' method="POST">
    <button class='button button3' style='margin-top:0.5cm;' type="submit">Dodaj v seznam</button>
</form>
