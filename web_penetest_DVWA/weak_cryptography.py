import requests
from bs4 import BeautifulSoup
import base64

DVWA_URL = "http://localhost/DVWA"
LOGIN_URL = f"{DVWA_URL}/login.php"
SECURITY_URL = f"{DVWA_URL}/security.php"
CRYPTO_URL = f"{DVWA_URL}/vulnerabilities/cryptography/"

USERNAME = "admin"
PASSWORD = "password"

session = requests.Session()

def login():
    print("[*] Logowanie do DVWA jako gordonb...")
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
    print(f"[+] Zalogowano jako {USERNAME}.")

def set_security_low():
    print("[*] Ustawianie poziomu bezpieczeństwa na LOW...")
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
        print("[+] Poziom bezpieczeństwa ustawiony na LOW.")
    else:
        print("[-] Nie udało się ustawić poziomu bezpieczeństwa.")

def exploit_cryptography():
    known_plaintext = "helloworld"
    print(f"[*] Wysyłanie znanej wiadomości do modułu Cryptography: {known_plaintext}")
    payload = {
        "message": known_plaintext,
        "direction": "encode"
    }

    r = session.post(CRYPTO_URL, data=payload)
    soup = BeautifulSoup(r.text, "html.parser")
    encoded = soup.find("textarea", {"id": "encoded"}).text.strip()
    print(f"[+] Zakodowana wiadomość: {encoded}")

    decoded = base64.b64decode(encoded)
    xor_key = ''.join(chr(decoded[i] ^ ord(known_plaintext[i])) for i in range(len(known_plaintext)))
    print(f"[+] Odzyskany klucz XOR: {xor_key}")

    print("[*] Pobieranie przechwyconej wiadomości...")
    r = session.get(CRYPTO_URL)
    soup = BeautifulSoup(r.text, "html.parser")

    textareas = soup.find_all("textarea")
    intercepted = None
    for textarea in textareas:
        if "Your new password" not in textarea.text and len(textarea.text.strip()) > 0:
            intercepted = textarea.text.strip()

    if not intercepted:
        print("[-] Nie udało się znaleźć przechwyconej wiadomości.")
        return

    print(f"[+] Przechwycona wiadomość (Base64): {intercepted}")

    intercepted_bytes = base64.b64decode(intercepted)
    key_bytes = xor_key.encode()

    decrypted = ''.join(chr(intercepted_bytes[i] ^ key_bytes[i % len(key_bytes)]) for i in range(len(intercepted_bytes)))
    print(f"[+] Odszyfrowana wiadomość:\n{decrypted}")

if __name__ == "__main__":
    login()
    set_security_low()
    exploit_cryptography()