import requests
from bs4 import BeautifulSoup

LOGIN_URL = "http://localhost/DVWA/login.php"
SECURITY_URL = "http://localhost/DVWA/security.php"
WEAK_ID_URL = "http://localhost/DVWA/vulnerabilities/weak_id/"
USERNAME = "admin"
PASSWORD = "password"

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

def test_weak_session_ids(count=10):
    print(f"[*] Testowanie podatności Weak Session ID ({count} prób)...")
    session_ids = []

    for i in range(count):
        r = session.post(WEAK_ID_URL)
        cookie = session.cookies.get("dvwaSession")
        print(f"[{i+1}] Otrzymany dvwaSession ID: {cookie}")
        session_ids.append(int(cookie))

    print("\n[*] Analiza wzoru sesji:")
    diffs = [session_ids[i+1] - session_ids[i] for i in range(len(session_ids)-1)]
    predictable = all(diff == 1 for diff in diffs)

    if predictable:
        print("[!] Identyfikatory sesji są inkrementowane → podatność POTWIERDZONA.")
    else:
        print("[+] Identyfikatory sesji nie są bezpośrednio przewidywalne.")

if __name__ == "__main__":
    login()
    set_security_low()
    test_weak_session_ids()