from Crypto.PublicKey import RSA
from Crypto.Hash import MD2
from Crypto.Signature import pkcs1_15


def rsa_sign_and_verify():
    print("=== RSA Digital Signature with MD2 ===")

    # 1. Generate RSA keys (3072 bits as required)
    key = RSA.generate(3072)
    private_key = key
    public_key = key.publickey()

    print(f"Key size: {key.size_in_bits()} bits")

    # 2. Message (from Lab2)
    m = (
        b"The addition of secrecy to the transformations produced cryptography. True, it was more of\n"
        b"a game than anything else \xe2\x80\x94 it sought to delay comprehension for only the shortest possible\n"
        b"time, not the longest \xe2\x80\x94 and the cryptanalysis was, likewise, just a puzzle. Egypt\xe2\x80\x99s was thus\n"
        b"a quasi cryptology in contrast to the deadly serious science of today. Yet great things have\n"
        b"small beginnings, and these hieroglyphs did include, though in an imperfect fashion, the\n"
        b"two elements of secrecy and transformation that comprise the essential attributes of the\n"
        b"science. And so cryptology was born. In its first 3,000 years, it did not grow steadily.\n"
        b"Cryptology arose independently in many places, and in most of them it died the deaths\n"
        b"of its civilizations. In other places, it survived, embedded in a literature, and from this the\n"
        b"next generation could climb to higher levels. But progress was slow and jerky. More was\n"
        b"lost than retained. Much of the history of cryptology of this time is a patchwork, a crazy\n"
        b"quilt of unrelated items: sprouting, flourishing, withering. Only toward the Western Renais-\n"
        b"sance does the accreting knowledge begin to build up a momentum. The story of cryptology\n"
        b"during these years is, in other words, exactly the story of mankind. China, the only high\n"
        b"civilization of antiquity to use ideographic writing, seems never to have developed much\n"
        b"real cryptography \xe2\x80\x94 perhaps for that reason. In one case known for military purposes,\n"
        b"the 11th-century compilation Wu-ching tsung-yao (\xe2\x80\x9cEssentials from Military Classics\xe2\x80\x9d) rec-\n"
        b"ommended a true, if small, code. To a list of 40 plaintext items, ranging from requests for\n"
        b"bows and arrows to the report of a victory, the correspondents would assign the first 40\n"
        b"ideograms of a poem. Then, when a lieutenant wished, for example, to request more arrows,\n"
        b"he was to write the corresponding ideogram at a specified place on an ordinary dispatch\n"
        b"and stamp his seal on it.\n\n"
        b"In China\xe2\x80\x99s great neighbor to the west, India \xe2\x80\x94 whose civilization likewise developed early\n"
        b"and to high estate \xe2\x80\x94 several forms of secret communications were known and apparently\n"
        b"practiced. The Artha-sastra, a classic work on statecraft attributed to Kautilya, in describing\n"
        b"the espionage service of India as practically riddling the country with spies, recommended\n"
        b"that the officers of the institutes of espionage give their spies their assignments by secret\n"
        b"writing.\n\n"
        b"Perhaps most interesting to cryptologists \xe2\x80\x94 amateur or professional \xe2\x80\x94 is that Vatsyayana\xe2\x80\x99s\n"
        b"famous textbook of erotics, the Kamasutra, lists secret writing as one of the 64 arts, or yogas,\n"
        b"that women should know and practice."
    )

    print(f"Message: {m.decode()}")

    # 3. Hash with MD2
    h = MD2.new(m)
    print(f"MD2 hash: {h.hexdigest()}")

    # 4. Sign the hash
    signature = pkcs1_15.new(private_key).sign(h)
    print(f"Signature (hex): {signature.hex()}")

    # 5. Verify signature
    try:
        pkcs1_15.new(public_key).verify(h, signature)
        print("Signature verification: SUCCESS")
        return True
    except Exception as e:
        print(f"Signature verification: FAILED - {e}")
        return False


if __name__ == "__main__":
    rsa_sign_and_verify()
