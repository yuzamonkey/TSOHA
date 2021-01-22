# Tapahtumakalenteri

Tietokantasovellus tapahtumien mainostamiseen ja tapahtumien etsimiseen. Tapahtumia voivat olla mm. konsertit, näyttelyt ja teatteriesitykset.

Sivulla ilman käyttäjätunnusta vieraileva näkee etusivulla tulevat tapahtumat. Ajatus olisi, että käyttäjälle avautuu näkymä kuukausikalenterista, jossa päivää klikkaamalla kalenterin viereen avautuu lista kyseisen päivän tapahtumista. Tiettyä tapahtumaa klikkaamalla käyttäjä ohjataan tapahtuman sivulle, johon on koottu olennainen tieto kyseisestä tapahtumasta, kuten tapahtuman nimi, kuvaus, järjestäjä, ajankohta, sijainti ja hinta. Etusivulla voi suodattaa hakutuloksia ajankohdan, kategorian, hinnan tai sijainnin perusteella.

Käyttäjätunnuksen luonut henkilö voi lisätä, muokata ja poistaa omia tapahtumia. Tapahtuman lisäys onnistuu kaavakkeen avulla. Käyttäjä voi myös raportoida ylläpitoon väärinkäytöstä tai spämmeistä.

Ylläpitäjän oikeuksilla voi lisätä ja poistaa mitä tahansa tapahtumia, tutkia tilastoja, sekä jäädyttää ja poistaa tilejä.

## Ominaisuudet
	* Ylläpitäjän ja käyttäjän oikeudet
	* Käyttäjätunnuksen luominen
	* Tapahtumien lisäys, poistaminen ja muokkaaminen
	* Väärinkäytön raportointi ylläpitäjälle
	* Tilastointi
	* Tapahtumien haku hakukriteereillä

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
	* Cities
	* Images

## Linkit
	Heroku-linkki, kun sovellus on valmiina julkaistavaksi