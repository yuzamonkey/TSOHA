# Tapahtumakalenteri

https://tapahtumakalenteri.herokuapp.com/ (päivitetty 6.3.2020)

Tietokantasovellus tapahtumien mainostamiseen ja tapahtumien etsimiseen. Tapahtumia voivat olla mm. konsertit, näyttelyt ja teatteriesitykset.

Sovellus on harjoitustyö HY:n kurssille Tietokantasovellus.

### Sovelluksen nykyinen tilanne 

Sovelluksen perustoiminnallisuudet ovat tehty. Merkittävät sovelluksen käyttöön kohdistuvat bugit on paikattu. CSS:ää lisätty kaikille sivuille. Tällä hetkellä bugeja ei ole tiedossani, joten jos testaat sovellusta ja löydät korjattavaa, postaisitko issuen.

Pientä hiottavaa:
- CSS ja HTML siistimistä
- Muutama metodi on moduuleissaan epäjohdonmukaisesti
 
 ### Testaus Herokussa
    
Ylläpitäjän tunnus ja salasana on admin. Ylläpitäjän työkalut löytyvät Omat tiedot -> admin työkalut. Peruskäyttäjän toimintojen tutkimista varten voi luoda uuden käyttäjätilin. Jos jostain syystä uuden käyttäjän luominen ei onnistu, sovellukseen voi kirjautua kombolla username-password.

## Kuvaus
  
  **Sivulla ilman käyttäjätunnusta vieraileva**
  - näkee etusivulla tulevat tapahtumat listanäkymästä
  - ohjataan tapahtuman sivulle, kun vierailija klikkaa tapahtumaa
  - voi hakea tapahtumia ajankohdan, kategorian tai sijainnin perusteella
  
  **Käyttäjätunnuksella kirjautunut käyttäjä voi**
  - lisätä, muokata ja poistaa omia tapahtumia
    - tapahtuma luodaan täyttämällä kaavake. Kaavakkeeseen tulee täyttää tapahtuman nimi, kuvaus, kategoria, ajankohta, sijainti ja hinta. Tapahtumaan voi lisätä kuvan.
  - raportoida ylläpitoon ongelmista
  
  **Ylläpitäjä voi**
  - lisätä, muokata tai poistaa minkä tahansa tapahtuman
  - lukea käyttäjien lähettämiä raportteja
  - tutkia tilastoja
  - jäädyttää ja poistaa tilejä

## Ominaisuudet
  - Ylläpitäjän ja käyttäjän oikeudet
  - Tilien jäädytys ja toiminnallisuuksien rajoittaminen
  - Käyttäjätunnuksen luominen
  - Tapahtumien lisäys, poistaminen ja muokkaaminen
  - Raportointi ylläpitäjälle
  - Tilastointi
  - Tapahtumien haku hakukriteereillä

## Käytetyt teknologiat
* Python
* Flask
* PostgreSQL
* Heroku
* HTML
* CSS
* JavaScript

## SQL-taulut
* Users
* Events
* Categories
* Counties
* Images
* Reports

## Linkit
https://tapahtumakalenteri.herokuapp.com/