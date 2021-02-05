# Tapahtumakalenteri

https://tapahtumakalenteri.herokuapp.com/

Tietokantasovellus tapahtumien mainostamiseen ja tapahtumien etsimiseen. Tapahtumia voivat olla mm. konsertit, näyttelyt ja teatteriesitykset.

## Kuvaus
  
  **Sivulla ilman käyttäjätunnusta vieraileva**
  - näkee etusivulla tulevat tapahtumat listanäkymästä
  - ohjataan tapahtuman sivulle, kun vierailija klikkaa tapahtumaa
  - voi hakea tapahtumia ajankohdan, kategorian, hinnan tai sijainnin perusteella
  
  **Käyttäjätunnuksella kirjautunut käyttäjä voi**
  - lisätä, muokata ja poistaa omia tapahtumia
    - tapahtuma luodaan täyttämällä kaavake. Kaavakkeeseen tulee täyttää tapahtuman nimi, kuvaus, kategoria, ajankohta, sijainti ja hinta. Tapahtumaan voi lisätä kuvan.
  - raportoida ylläpitoon ongelmista
  
  **Ylläpitäjä voi**
  - lisätä tai poistaa minkä tahansa tapahtuman
  - lukea käyttäjien lähettämiä raportteja
  - tutkia tilastoja
  - jäädyttää ja poistaa tilejä

## Ominaisuudet
  - Ylläpitäjän ja käyttäjän oikeudet
  - Käyttäjätunnuksen luominen
  - Tapahtumien lisäys, poistaminen ja muokkaaminen
  - Väärinkäytön raportointi ylläpitäjälle
  - Tilastointi
  - Tapahtumien haku hakukriteereillä

## Käytetyt teknologiat
* Python
* Flask
* PostgreSQL
* Heroku
* HTML
* CSS

## SQL-taulut
* Users
* Events
* Categories
* Counties
* Images
* Reports

## Linkit
https://tapahtumakalenteri.herokuapp.com/