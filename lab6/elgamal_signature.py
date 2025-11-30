"""
ElGamal Digital Signature with MD5 Hash
Laboratory Work #6
"""

import random
import math
from hashlib import md5


def elgamal_sign_and_verify():
    print("=== ElGamal Digital Signature with MD5 ===")

    # 1. p and g (given in the task)
    # Large 2048-bit prime p
    p = 32317006071311007300153513477825163362488057133489075174588434139269806834136210002792056362640164685458556357935330816928829023080573472625273554742461245741026202527916572972862706300325263428213145766931414223654220941111348629991657478268034230553086349050635557712219187890332729569696129743856241741236237225197346402691855797767976823014625397933058015226858730761197532436467475855460715043896844940366130497697812854295958659597567051283852132784468522925504568272879113720098931873959143374175837826000278034973198552060607533234122603254684088120031105907484281003994966956119696956248629032338072839127039

    g = 2

    print(f"Prime p: {p} ({p.bit_length()} bits)")
    print(f"Generator g: {g}")

    # 2. Private and public keys
    x = random.randint(2, p - 2)  # private key
    y = pow(g, x, p)  # public key

    print(f"Private key x: {x}")
    print(f"Public key y: {y}")

    # 3. Message
    m = b"This is a test message for digital signature demonstration in Laboratory Work #6"
    print(f"Message: {m.decode()}")

    # 4. Hash with MD5
    hash_obj = md5(m)
    hm = int.from_bytes(hash_obj.digest(), "big")
    print(f"MD5 hash (decimal): {hm}")

    # 5. Choose k
    while True:
        k = random.randint(2, p - 2)
        if math.gcd(k, p - 1) == 1:
            break

    print(f"Random k: {k}")

    # 6. Calculate signature
    r = pow(g, k, p)
    k_inv = pow(k, -1, p - 1)  # Modular inverse of k mod (p-1)
    s = ((hm - x * r) * k_inv) % (p - 1)

    print(f"Signature (r, s): r={r}, s={s}")

    # 7. Verification
    left = pow(g, hm, p)
    right = (pow(y, r, p) * pow(r, s, p)) % p

    is_valid = left == right
    print(f"Verification: left={left}")
    print(f"Verification: right={right}")
    print(f"Signature valid: {is_valid}")

    return is_valid


if __name__ == "__main__":
    elgamal_sign_and_verify()
