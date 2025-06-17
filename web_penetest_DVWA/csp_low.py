import requests
from bs4 import BeautifulSoup

CSP_URL = "http://localhost/DVWA/vulnerabilities/csp/"
LOGIN_URL = "http://localhost/DVWA/login.php"
SECURITY_URL = "http://localhost/DVWA/security.php"
USERNAME = "admin"
PASSWORD = "password"

session = requests.Session()

def login():
    """Logowanie do DVWA."""
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
    """Ustawienie poziomu zabezpieczeń na LOW."""
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

def get_csp_header(url):
    try:
        response = session.get(url)

        if 'Content-Security-Policy' in response.headers:
            return response.headers['Content-Security-Policy']
        else:
            return "Nagłówek CSP nie jest ustawiony na tej stronie."
    
    except requests.exceptions.RequestException as e:
        return f"Błąd: {e}"

if __name__ == "__main__":
    login()
    set_security_low()

    print("\n[*] Pobieranie nagłówka CSP...")
    csp_header = get_csp_header(CSP_URL)
    print(f"Nagłówek CSP: {csp_header}")