# WakaFree (v. 1.3.3)

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

`python WakaFree.py [-h] [-g GRAPHS] [-t TOTALS] FILE`

The arguments in the square brackets are optional. The arguments are explained below:
- -h / --help: Prints information about the program. With this argument, the positional argument FILE is not required.
- -g / --graphs: Draws the graphs for daily stats. Use a string with l or L for programming languages, e or E for editors and o or O for operating systems.
- -t / --totals: Shows total times. Use a string with l or L for programming languages, e or E for editors and o or O for operating systems.
- FILE: The path for the file that contains the statistics from WakaTime. Can be downloaded from WakaTime by going to Settings &#8594; Personal settings &#8594; Account &#8594; Export.

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

`python WakaFree.py [-h] [-g GRAPHS] [-t TOTALS] FILE`

Hakasulkeissa olevat argumentit eivät ole pakollisia. Argumentit on selitetty alapuolella:
- -h / --help: Tulostaa tietoja ohjelmasta. Tämän argumentin kanssa argumentti FILE ei ole tarpeellinen.
- -g / --graphs: Piirtää kuvaajat päivittäisten tietojen perusteella. Käytä merkkijonoa, jossa on l tai L ohjelmointikieliä varten, e tai E editoreja varten ja o tai O käyttöjärjestelmiä varten.
- -t / --totals: Näyttää kokonaisajat. Käytä merkkijonoa, jossa on l tai L ohjelmointikieliä varten, e tai E editoreja varten ja o tai O käyttöjärjestelmiä varten.
- FILE: Polku tiedostoon, joka sisältää WakaTimen tilastot. Voidaan ladata WakaTimesta kohdasta Settings &#8594; Personal settings &#8594; Account &#8594; Export.