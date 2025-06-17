# 🔐 Web Pentest Automation – DVWA

Projekt realizowany w środowisku Kali Linux z użyciem aplikacji **DVWA (Damn Vulnerable Web Application)**. Zautomatyzowaliśmy identyfikację i eksploatację licznych podatności aplikacji webowej poprzez własne skrypty w Pythonie.

---

## 🎯 Cel projektu

Celem naszego projektu była analiza i praktyczne wykorzystanie podatności zawartych w aplikacji DVWA. Skupiliśmy się na:

- Identyfikacji jak największej liczby podatności,
- Zrozumieniu mechanizmów ich działania,
- Opracowaniu skutecznych metod ich eksploitacji,
- Automatyzacji ataków przy użyciu własnych skryptów.

---

## 🧪 Środowisko testowe

- Maszyna wirtualna: **Kali Linux**
- Aplikacja testowa: **DVWA (Damn Vulnerable Web Application)**
- Edytor kodu: **Visual Studio Code**
- Narzędzia użyte w analizach:
  - `Burp Suite`, `OWASP ZAP`, `curl`, `wget`
  - Automatyzacja: `Python`, `Hydra`, `SQLMap`

---

## 📦 Instalacja

1. Skonfiguruj środowisko:
   - Zainstaluj **DVWA** na maszynie wirtualnej
   - Użyj **Kali Linux** lub innego środowiska testowego

2. Zainstaluj wymagane biblioteki Pythona:

```bash
pip install -r requirements.txt
```

3. Zainstaluj dodatkowe narzędzia używane w skryptach:

- **Hydra** (do ataków brute-force)
- **sqlmap** (do automatycznego testowania SQL Injection)

```bash
sudo apt update
sudo apt install hydra sqlmap
```

---

## ⚙️ Automatyzacja

Wiele ataków zostało w pełni **zautomatyzowanych** z wykorzystaniem skryptów Python. Każdy z nich:

- Loguje się na DVWA (z użyciem CSRF tokena),
- Ustawia poziom zabezpieczeń na `low`,
- Przeprowadza konkretny atak związany z podatnością.

Przykłady automatyzacji:

- **Brute Force (`brute_force_low.py`)**:
  - Skrypt loguje się i ustawia poziom zabezpieczeń na `low`
  - Pobiera `PHPSESSID`
  - Używa `Hydra` do przeprowadzenia ataku słownikowego (z plikiem `rockyou.txt`)

- **Weak Session ID (`week_session_id_low.py`)**:
  - Loguje się, ustawia poziom `low`
  - Generuje wielokrotnie sesje i analizuje przewidywalność ID
  - Identyfikuje inkrementację → podatność potwierdzona

- **Auth Bypass (`auth_bypass.py`)**:
  - Wykonuje rekursywne skanowanie ścieżek (do głębokości 2)
  - Sprawdza odpowiedzi HTTP dla potencjalnych endpointów umożliwiających obejście autoryzacji
  - Identyfikuje potencjalne bypassy na podstawie wzorców w URL-ach

- **Command Injection (`command_injection_low.py`)**:
  - Automatycznie wstrzykuje polecenie do formularza (np. `127.0.0.1; id`)
  - Parsuje wynik wykonania komendy z odpowiedzi HTML (`<pre>`)
  - Informuje, czy atak się powiódł i wyświetla wynik polecenia

- **CSP Header Check (`csp_low.py`)**:
  - Wysyła żądanie do strony podatnej na błędną konfigurację CSP
  - Odczytuje nagłówek `Content-Security-Policy` z odpowiedzi
  - Informuje, czy nagłówek jest obecny i jak wygląda

- **Open Redirect (`open_http_redirected.py`)**:
  - Wyszukuje link z parametrem `redirect` na stronie podatnej
  - Modyfikuje go tak, by wskazywał na `http://download.zip?id=1`
  - Wysyła żądanie bez automatycznego podążania za przekierowaniem
  - Analizuje nagłówek `Location` i potwierdza obecność podatności na Open Redirect

- **Blind SQL Injection (`sql_injection_blind_low.py`)**:
  - Używa `sqlmap` z wymuszoną techniką Blind SQLi (`--technique B`)
  - Pobiera listę baz danych, tabele z bazy `dvwa` i zrzuca zawartość tabeli `users`

- **Classic SQL Injection (`sql_injection_low.py`)**:
  - Wykorzystuje `sqlmap` do klasycznego SQL Injection
  - Pobiera bazy danych, tabele i zrzuca dane z tabeli `users`

- **Weak Cryptography (`weak_cryptography.py`)**:
  - Wysyła znany plaintext do modułu kryptografii DVWA i analizuje zakodowany wynik
  - Odzyskuje klucz XOR i używa go do odszyfrowania przechwyconej wiadomości
  - Demonstruje słabość zastosowanej kryptografii (XOR + Base64)
 
- **DOM-Based XSS (`xss_dom_low.py`)**:
  - Tworzy payload kradnący ciasteczko i przesyła je na serwer atakującego (`http.server`)
  - Otwiera przeglądarkę z odpowiednio spreparowanym adresem URL
  - Wyświetla również zakodowany adres do debugowania

- **Reflected XSS (`xss_reflected_low.py`)**:
  - Generuje link zawierający złośliwy payload JavaScript
  - Wysyła żądanie GET i sprawdza obecność payloadu w odpowiedzi DVWA
  - Parsuje sekcję `vulnerable_code_area`, by potwierdzić skuteczność ataku

- **Stored XSS (`xss_stored_low.py`)**:
  - Wysyła złośliwy komentarz zawierający JavaScript do księgi gości DVWA
  - Weryfikuje, czy payload pojawia się w odpowiedzi HTML
  - Automatyzuje cały proces wstawienia i detekcji ataku trwałego XSS

---

**Każdy skrypt można uruchomić niezależnie (przykład poniżej):**

```bash
python3 brute_force_low.py
```

---

## 🖼️ Prezentacja

📎 Plik **Prezentacja_DVWA_Pentest.pptx** zawiera slajdy użyte do przedstawienia projektu.

📎 Plik **DVWA_dokumentacja.pdf** zawiera pełny opis wszystkich czynności wykonanych podczas projektu, w tym opis podatności, opis automatyzacji, wstęp, cel oraz wnioski.

📎 Plik **video_prezentacja.mp4** to nagranie naszej prezentacji wyników projektu. Znajduję się ono na platformie youtube pod linkiem: https://youtu.be/CdJFEY1F1kw z powodu wielkości pliku.
