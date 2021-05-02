% rebase('osnova.tpl')

<h1>NUT.TRACKER</h1>

<form action="/prijava/" method="POST">

  <div class="container">
    <label for="username"><b>Uporabniško ime</b></label>
    <input type="text" placeholder="Vpišite uporabniško ime" name="ime" required>

    <br>
    <label for="password"><b>Geslo</b></label>
    <input type="password" placeholder="Vpišite geslo" name="geslo" required>

    <br>
    <button class='button button1' type="submit">Prijava</button>
  </div>

  <div class="center">
      <p>Še nimate računa?  <b><a href="/vpis/">Vpis</a></b></p>
  </div>
</form> 
