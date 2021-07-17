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
        <label for="hrana"><b>Hrana: </b></label>
        <input type="text2" name="hrana" required><br>
        <br>
        <label for="gram"><b>Količina: </b></label>
        <input type="number" name="gram" required> g
        
        <br>
        <button class='button button1' type="submit">Dodaj</button>
    </form>
</div>

<p style='font-size:12px; color:indigo; text-align:center'>Navedene jedi ni na seznamu hrane. Dodajte jo s klikom na spodnji gumb.</p>
<form action='/odpri_na_seznam/' method="POST">
    <button class='button button3' type="submit">Dodaj v seznam</button>
</form>
