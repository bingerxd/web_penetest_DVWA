import requests
from bs4 import BeautifulSoup

LOGIN_URL = "http://localhost/DVWA/login.php"
SECURITY_URL = "http://localhost/DVWA/security.php"
BASE_URL = "http://localhost/DVWA"
WORDLIST_FILE = "auth_bypass_worldlist.txt"

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

def recursive_scan(base_url, wordlist_file, depth=2):
    with open(wordlist_file, "r") as f:
        paths = [line.strip() for line in f.readlines()]

    def scan_level(url, current_depth):
        if current_depth == 0:
            return
        for path in paths:
            full_url = f"{url}/{path}/"
            try:
                r = session.get(full_url)
                if r.status_code == 200:
                    print(f"[+] Znaleziono: {full_url}")
                    if "authbypass" in full_url:
                        print(f"[!!!] Możliwy bypass autoryzacji: {full_url}")
                    scan_level(full_url.rstrip('/'), current_depth - 1)
            except requests.RequestException as e:
                print(f"[-] Błąd przy {full_url}: {e}")

    print(f"\n[*] Rozpoczynanie rekursywnego skanowania od {base_url}...")
    scan_level(base_url, depth)

if __name__ == "__main__":
    login()
    set_security_low()
    recursive_scan(BASE_URL, WORDLIST_FILE, depth=2)