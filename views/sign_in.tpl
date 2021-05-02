% rebase('osnova.tpl')

<h1>NUT.TRACKER</h1>

<form action="/vpis/" method="POST">
  <div class="container">
    <label for="username"><b>Uporabniško ime</b></label>
    <input type="text" placeholder="Vpišite uporabniško ime" name="ime" required>

    <br>
    <label for="password"><b>Geslo</b></label>
    <input type="password" placeholder="Vpišite geslo" name="geslo" required>

  </div>

  <div class="container-small">
    <b>Spol</b>
    <div class="radio-input">
      <input type="radio" id="moski" name="spol" value="M">
      <label for="moski"><p>M</p></label>
      <input type="radio" id="zenski" name="spol" value="Ž">
      <label for="zenski"><p>Ž</p></label>
    </div>
    
    <b>Teža: </b><input type="number" min="1" name='teza'>
    
    <br><br>
    <b>Visina:  </b><input type="number" min="1" name='visina'>

    <br><br>
    <b>Starost:   </b><input type="number" min="1" name='starost'>
    
    <br><br>
    <table style='width:50%'>
      <tr>
        <td width='30%'><b>Aktivnost:</b></td>
        <td width='70%'>
          <select name="aktivnost">
            <option value="nič">nič</option>
            <option value="1-2 dni">1-2 dni</option>
            <option value="3-5 dni">3-5 dni</option>
            <option value="6-7 dni">6-7 dni</option>
            <option value="2-krat dnevno">2-krat dnevno</option>
          </select>
        </td>
      </tr>
    </table>  
  </div>

  <button class='button button2' type="submit">Vpis</button>
</form> 
