O projektu:

Projekt TBR Place jsou stránky kde si uživatelé na základě předdefinovaných promptů mohou vyhledávat knížky.
Stránky jsou napojené prostřednictvím api na open library. Uživatelé si mohou prompty generovat,
mohou se zaregistrovat a vytvořit si vlastní profil, kde si pak mohou prompty a knižní díla přidávat, mazat
a upravovat. Díla mohou také komentovat. Mohou kometnovat a hodnotit ratingem své přidané knihy a knihy ostatních uživatelů.
Stránky obsahují také diskuzní forum, kde uživatelé mohou vytvářet přispěky a vlákna.

1.klonujte tento repozitář:

git clone https://github.com/Prexus6/tbr_place_project.git

2.projekt spustíte příkazem python manage.py runserver
ve složce tbr_place_project

3. nainstalujte potřebné requirements příkazem pip install -r requirements.txt
4. proveďte migrace databáze: python manage.py migrate
5. spusťte vývojový server: python manage.py runserver
6. Otevřete webový prohlížeč a přejděte na adresu http://127.0.0.1:8000/

7. Aplikace:
tbr_place: 
- sekce generování náhodných promptů+možnost filtrovaného generování podle typu promptů, 
- sekce uživatelských promptů(možnost vytvořit vlastní typy promptů, 
- možnost vytvožit vlastní prompt zařazený pod vlastní typ promptu)
- sekce vytvoření vlastní databáze náhledů vytvořených promptů, kde může je upravovat, mazat
- sekce generování uživatelských promptů podle zvoleného filtru uživatelských typů promptů 
- sekce random code generator . vygenruje náhodný knižní/motivační citát  
- sekce book search - slouží na vyhledávání knih, podle možných volitelných filtračních parametrů(book title, genre, author name)
pomoci Api Open Library https://openlibrary.org/developers/api

literary_works(backend pracuje přes python ve spolupráci s javascriptovými dynamickými funkcemi:
url: path('literary-works/', include('literary_works.urls')),
url: path('api/', include('literary_works.urls')),
- sekce náhledu uživatelských vlastních literárních prací - filtrování podle kategorií, filtrace zobrazení podle datumu, podle hodnocení, podle nejvíce hodnocených,
  (defaultně je všechno zařazené podle datumu), tlačítko pro přidaní nové uživatelovi literární práce, zobrazené díla obsahují autora(uživatelský autor), kategorii(díla, průměrné hodnocení díla, počet hodnocení díla, počet komentářů, možnost read more)
- sekce read more - pokud se jedná o dílo uživatelě má možnost dílo editovat(zakomponovaná možnost použití formátování přes markdown) nebo mazat(zabezpečené výzvou zadání uživatelského hesla), odpovědět na komentáře jiných uživatelů,
- sekce přidávání uživatelského díla uživatelů - možnost zadat název a kraátký popis díla, možnost vložení obsahu díla, možnost přidání fotky díla, možnost zařazení do kategorie, 
- sekce uživatelského profilu - jedná se o náhled zobrazení všech uživatelových jeho vlastních literárních prací a děl, možnost přímého přidávání děl, možnost přístupu ke svým dílům a jejich upravování
- 

accounts: stará se o registraci a přihlšování uživatelů
url: path('accounts/', include('accounts.urls')),
- obsahuje možnost přihlášení uživatele, odhlášení, obnovy hesla, nastavení tajné otázky místo registrace emailem,
nastavení nového hesla, registrace nového uživatele, resetování hesla, (povinné nastavení security question))

forum: diskuzní forum na jakékoliv téma dostupné pro registraci
url: path('forum/', include('forum.urls')),
- obsahuje možnost přidání příspěvku, editování, mazání, možnost komentovat příspěvky
- uživatel může vidět i přispěvky které komentoval a upravovat komentáře, pod každým uživatelem je uložena jeho historie na forumu

8. Kontakt:
email na správce:
9. Contributori: Filip Húšťava, Ondřej Kříž


