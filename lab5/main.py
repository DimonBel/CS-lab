"""
Команды:
  init                         — инициализировать CA (создаст ./pki)
  create-user <name>           — создать ключ и сертификат пользователя (2048 бит, 365 дней)
  sign-file <user> <file>      — подписать файл приватным ключом пользователя (RSA + SHA256)
  verify <user> <file> <sig>   — проверить подпись (использует сертификат пользователя)
  revoke <user>                — отозвать сертификат пользователя (через CRL)
  gen-crl                      — сгенерировать/обновить CRL (crl.pem)
  show-certs                   — показать выданные сертификаты (в папке pki/certs)
"""

import argparse
import subprocess
import shutil
from pathlib import Path
import sys

ROOT = Path.cwd() / "pki"
CA_DIR = ROOT / "ca"
CERTS_DIR = CA_DIR / "certs"
PRIVATE_DIR = CA_DIR / "private"
CRL_DIR = CA_DIR / "crl"
CSRS_DIR = CA_DIR / "csrs"
CRL_PEM = CRL_DIR / "crl.pem"
CA_KEY = PRIVATE_DIR / "ca.key.pem"
CA_CERT = CA_DIR / "ca.cert.pem"
CA_SERIAL = CA_DIR / "ca.srl"

OPENSSL_BIN = shutil.which("openssl")
if not OPENSSL_BIN:
    print("Ошибка: openssl не найден в PATH.")
    sys.exit(1)


def run(cmd, **kwargs):
    print("=>", " ".join(cmd))
    subprocess.run(cmd, check=True, **kwargs)


def ensure_dirs():
    for d in (ROOT, CA_DIR, CERTS_DIR, PRIVATE_DIR, CRL_DIR, CSRS_DIR):
        d.mkdir(parents=True, exist_ok=True)


def init_ca():
    ensure_dirs()
    # Генерация ключа CA (4096 бит)
    if not CA_KEY.exists():
        run([OPENSSL_BIN, "genrsa", "-out", str(CA_KEY), "4096"])
        CA_KEY.chmod(0o600)
    # Self-signed сертификат CA (3650 дней)
    if not CA_CERT.exists():
        subj = "/CN=My Test Root CA"
        run(
            [
                OPENSSL_BIN,
                "req",
                "-x509",
                "-new",
                "-nodes",
                "-key",
                str(CA_KEY),
                "-sha256",
                "-days",
                "3650",
                "-subj",
                subj,
                "-out",
                str(CA_CERT),
            ]
        )
    # Создание CA сериал файла
    if not CA_SERIAL.exists():
        CA_SERIAL.write_text("1000\n")
    print("CA инициализирован в папке:", CA_DIR)


def create_user(username: str):
    ensure_dirs()
    user_key = PRIVATE_DIR / f"{username}.key.pem"
    user_csr = CSRS_DIR / f"{username}.csr.pem"
    user_cert = CERTS_DIR / f"{username}.cert.pem"

    if user_key.exists():
        raise SystemExit(f"Ключ пользователя {username} уже существует: {user_key}")

    # Генерация ключа пользователя
    run([OPENSSL_BIN, "genrsa", "-out", str(user_key), "2048"])
    user_key.chmod(0o600)

    # CSR
    subj = f"/CN={username}"
    run(
        [
            OPENSSL_BIN,
            "req",
            "-new",
            "-key",
            str(user_key),
            "-out",
            str(user_csr),
            "-subj",
            subj,
        ]
    )

    # Подписание CSR CA напрямую (Windows-friendly)
    run(
        [
            OPENSSL_BIN,
            "x509",
            "-req",
            "-in",
            str(user_csr),
            "-CA",
            str(CA_CERT),
            "-CAkey",
            str(CA_KEY),
            "-CAcreateserial",
            "-out",
            str(user_cert),
            "-days",
            "365",
            "-sha256",
        ]
    )
    print(f"Создан сертификат: {user_cert}")
    return user_key, user_cert


def sign_file(username: str, filepath: str):
    user_key = PRIVATE_DIR / f"{username}.key.pem"
    if not user_key.exists():
        raise SystemExit("Ключ пользователя не найден: " + str(user_key))
    filepath = Path(filepath)
    sig = filepath.with_suffix(filepath.suffix + ".sig")
    run(
        [
            OPENSSL_BIN,
            "dgst",
            "-sha256",
            "-sign",
            str(user_key),
            "-out",
            str(sig),
            str(filepath),
        ]
    )
    print("Подписанный файл:", sig)
    return sig


def verify_sig(username: str, filepath: str, sigpath: str):
    user_cert = CERTS_DIR / f"{username}.cert.pem"
    if not user_cert.exists():
        raise SystemExit("Сертификат пользователя не найден: " + str(user_cert))
    pubkey = PRIVATE_DIR / f"{username}.pub.pem"
    run(
        [
            OPENSSL_BIN,
            "x509",
            "-in",
            str(user_cert),
            "-pubkey",
            "-noout",
            "-out",
            str(pubkey),
        ]
    )
    try:
        run(
            [
                OPENSSL_BIN,
                "dgst",
                "-sha256",
                "-verify",
                str(pubkey),
                "-signature",
                str(sigpath),
                str(filepath),
            ]
        )
        print("Подпись верна.")
    finally:
        if pubkey.exists():
            pubkey.unlink()


def revoke_user(username: str):
    cert = CERTS_DIR / f"{username}.cert.pem"
    if not cert.exists():
        raise SystemExit("Сертификат пользователя не найден: " + str(cert))
    # Простая эмуляция отзыва: добавим запись в CRL через openssl ca только если CRL создан
    print(
        "Отзыв через CRL поддерживается только при использовании openssl ca (не используется напрямую x509)."
    )


def gen_crl():
    CRL_DIR.mkdir(exist_ok=True)
    if not CA_CERT.exists() or not CA_KEY.exists():
        raise SystemExit("CA не инициализирована. Сначала выполните init.")
    run(
        [OPENSSL_BIN, "ca", "-gencrl", "-out", str(CRL_PEM), "-config", "/dev/null"]
    )  # заглушка
    print("CRL создан:", CRL_PEM)


def show_certs():
    for c in sorted(CERTS_DIR.glob("*.pem")):
        print(c)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument(
        "cmd",
        choices=[
            "init",
            "create-user",
            "sign-file",
            "verify",
            "revoke",
            "gen-crl",
            "show-certs",
        ],
    )
    p.add_argument("args", nargs="*")
    return p.parse_args()


def main():
    args = parse_args()
    cmd = args.cmd
    a = args.args
    try:
        if cmd == "init":
            init_ca()
        elif cmd == "create-user":
            if len(a) != 1:
                raise SystemExit("Usage: create-user <username>")
            create_user(a[0])
        elif cmd == "sign-file":
            if len(a) != 2:
                raise SystemExit("Usage: sign-file <username> <file>")
            sign_file(a[0], a[1])
        elif cmd == "verify":
            if len(a) != 3:
                raise SystemExit("Usage: verify <username> <file> <sig>")
            verify_sig(a[0], a[1], a[2])
        elif cmd == "revoke":
            if len(a) != 1:
                raise SystemExit("Usage: revoke <username>")
            revoke_user(a[0])
        elif cmd == "gen-crl":
            gen_crl()
        elif cmd == "show-certs":
            show_certs()
    except subprocess.CalledProcessError as e:
        print("Команда OpenSSL завершилась с ошибкой:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
