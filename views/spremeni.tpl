% rebase('osnova.tpl')

<form class='alignright' action="/odjava/" method="POST" style='color:white'>
    <button class='button button4' type="submit" >Odjava</button>
</form>

<h1><div class='naslov-fp'>Osebni podatki<div></h1>

    <form action="/spremeni_podatke/{{ime_uporabnika}}/{{datum}}" method="POST">
        <div class="container-small">
          <b>Spol</b>
          <div class="radio-input">
            <input type="radio" id="moski" name="spol" value="M">
            <label for="moski"><p>M</p></label>
            <input type="radio" id="zenski" name="spol" value="Ž">
            <label for="zenski"><p>Ž</p></label>
          </div>
          
          <b>Teža: </b><input type="number" step="0.01" min="1" name='teza'><a> kg</a>
          
          <br><br>
          <b>Višina:  </b><input type="number" step="0.01" min="1" name='visina'><a> cm</a>
      
          <br><br>
          <b>Starost:   </b><input type="number" step="0.01" min="1" name='starost'><a> let</a>
          
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
      
        <button class='button button2' type="submit">Spremeni</button>
      </form> 