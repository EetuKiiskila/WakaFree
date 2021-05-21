# WakaFree (v. 1.10)

[English](#english)

[Suomi](#suomi)

![](https://i.imgur.com/a1OcuWY.png)

![](https://i.imgur.com/PUW7z5A.png)

## English

You can use this program to show your statistics from WakaTime. You can also save the figures drawn by the program. I do not encourage anyone to use this program. If you can afford it, you should consider supporting WakaTime.

### Requirements

- Python: I have version 3.9.0 installed. I haven't tested any other versions.
- PyYAML: I have version 5.4.1 installed. I haven't tested any other versions.
- NumPy: I have version 1.19.3 installed. Version 1.19.4 doesn't work. I haven't tested any other versions.
- Matplotlib: I have version 3.3.3 installed. I haven't tested any other versions.
- pandas: I have version 1.2.3 installed. I haven't tested any other versions.
- Plotly: I have version 4.14.3 installed. I haven't tested any other versions.

### Installation

Install the listed requirements. After that, clone the repository with the following command:

`git clone https://github.com/EetuKiiskila/WakaFree`

### Usage

`python WakaFree.py {-h | [-g GRAPHS] [-t TOTALS] [-i IGNORE] [--start-date START_DATE] [--end-date END_DATE] FILE}`

The arguments in the square brackets are optional. The arguments are explained below:
- -h / --help: Prints information about the program. With this argument, the positional argument FILE is not required.
- -g / --graphs: Draws the graphs for daily stats. Use a string with l or L for programming languages, e or E for editors and o or O for operating systems.
- -t / --totals: Shows total times. Use a string with l or L for programming languages, e or E for editors and o or O for operating systems.
- -i / --ignore: Ignores stats with given labels. Use a string with labels separated by commas and nothing more.
- --start-date: Shows all dates starting from the given date. Use a string in format "YYYY-MM-DD". Inclusive. Dates are not prepended to the stats if the given date is before the first date in the stats.
- --end-date: Shows all dates ending in the given date. Use a string in format "YYYY-MM-DD". Inclusive. Dates are not appended to the stats if the given date is after the last date in the stats.
- FILE: The path for the file that contains the statistics from WakaTime. Can be downloaded from WakaTime by going to Settings &#8594; Personal settings &#8594; Account &#8594; Export.

If neither of the optional arguments for drawing the charts is given with FILE, then everything will be drawn.

### Examples

The following command draws all the charts based on the stats from the file *stats.json*:

`python WakaFree.py stats.json`

The following command does the same:

`python WakaFree.py -g leo -t leo stats.json`

### Known issues

The program might not always manage to show the figures. This seems to be an issue with Plotly. In case this happens, simply run the program again. Having your default browser open might also help.

## Suomi

Voit käyttää tätä ohjelmaa WakaTimen keräämien tietojen näyttämiseen. Voit myös tallentaa ohjelman piirtämät kaaviot. En kannusta ketään käyttämään tätä ohjelmaa. Jos sinulla on varaa, kannattaa harkita WakaTimen tukemista rahallisesti.

### Vaatimukset

- Python: Minulla on asennettuna versio 3.9.0. En ole testannut muilla versioilla.
- PyYAML: Minulla on asennettuna versio 5.4.1. En ole testannut muilla versioilla.
- NumPy: Minulla on asennettuna versio 1.19.3. Versiolla 1.19.4 ei toimi. En ole testannut muilla versioilla.
- Matplotlib: Minulla on asennettuna versio 3.3.3. En ole testannut muilla versioilla.
- pandas: Minulla on asennettuna versio 1.2.3. En ole testannut muilla versioilla.
- Plotly: Minulla on asennettuna versio 4.14.3. En ole testannut muilla versioilla.

### Asennus

Asenna vaatimuksissa mainitut asiat. Sen jälkeen kopioi säilö tietokoneellesi seuraavalla komennolla:

`git clone https://github.com/EetuKiiskila/WakaFree`

### Käyttö

`python WakaFree.py {-h | [-g GRAPHS] [-t TOTALS] [-i IGNORE] [--start-date START_DATE] [--end-date END_DATE] FILE}`

Hakasulkeissa olevat argumentit eivät ole pakollisia. Argumentit on selitetty alapuolella:
- -h / --help: Tulostaa tietoja ohjelmasta. Tämän argumentin kanssa argumentti FILE ei ole tarpeellinen.
- -g / --graphs: Piirtää kuvaajat päivittäisten tietojen perusteella. Käytä merkkijonoa, jossa on l tai L ohjelmointikieliä varten, e tai E editoreja varten ja o tai O käyttöjärjestelmiä varten.
- -t / --totals: Näyttää kokonaisajat. Käytä merkkijonoa, jossa on l tai L ohjelmointikieliä varten, e tai E editoreja varten ja o tai O käyttöjärjestelmiä varten.
- -i / --ignore: Ohittaa tiedot annetuilla otsikoilla. Käytä merkkijonoa, jossa otsikot on erotettu toisistaan pelkillä pilkuilla.
- --start-date: Näyttää tiedot annetusta päivästä alkaen. Käytä muodossa "VVVV-KK-PP" olevaa merkkijonoa. Päivämäärä kuuluu piirrettävään väliin. Tyhjiä päiviä ei lisätä tilastojen alkuun, jos annettu päivämäärä on ennen tilastojen ensimmäistä päivää.
- --end-date: Näyttää tiedot annettuun päivään asti. Käytä muodossa "VVVV-KK-PP" olevaa merkkijonoa. Päivämäärä kuuluu piirrettävään väliin. Tyhjiä päiviä ei lisätä tilastojen loppuun, jos annettu päivämäärä on tilastojen viimeisen päivän jälkeen.
- FILE: Polku tiedostoon, joka sisältää WakaTimen tilastot. Voidaan ladata WakaTimesta kohdasta Settings &#8594; Personal settings &#8594; Account &#8594; Export.

Jos kumpaakaan valinnaista argumenttia kaavioiden piirtämiseen ei anneta FILE:n kanssa, piirretään kaikki kuvaajat.

### Esimerkkejä

Seuraava komento piirtää kaikki kuvaajat tiedoston *stats.json* sisältämistä tiedoista:

`python WakaFree.py stats.json`

Seuraava komento tekee saman:

`python WakaFree.py -g leo -t leo stats.json`

### Tiedossa olevat ongelmat

Ohjelma ei välttämättä aina onnistu näyttämään kaavioita. Ongelma vaikuttaa liittyvän Plotlyyn. Tällaisissa tapauksissa suorita ohjelma vain uudestaan. Oletusselaimen avaaminen ennen ohjelman suorittamista voi myös auttaa.