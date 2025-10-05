class VigenereCipher:
    def __init__(self):
        # Romanian alphabet with 31 letters (indexed 0-30)
        self.alphabet = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"
        self.alphabet_size = len(self.alphabet)

        # Dictionaries for quick conversion
        self.char_to_num = {char: i for i, char in enumerate(self.alphabet)}
        self.num_to_char = {i: char for i, char in enumerate(self.alphabet)}

    def validate_text(self, text):
        """Validate that text contains only allowed characters"""
        allowed_chars = set(self.alphabet + self.alphabet.lower() + " ")

        for char in text:
            if char not in allowed_chars:
                return (
                    False,
                    f"The character '{char}' is not allowed. Use only Romanian letters (A-Z, Ă, Â, Î, Ș, Ț) and spaces.",
                )
        return True, ""

    def validate_key(self, key):
        """Validate encryption key"""
        if len(key) < 7:
            return False, "The key must have at least 7 characters!"

        valid, msg = self.validate_text(key)
        if not valid:
            return False, f"The key contains invalid characters: {msg}"

        # Check that the key has no spaces
        if " " in key:
            return False, "The key cannot contain spaces!"

        return True, ""

    def prepare_text(self, text):
        """Prepare text: remove spaces and convert to uppercase"""
        text = text.replace(" ", "")
        text = text.upper()
        return text

    def encrypt(self, plaintext, key):
        """Encrypt message using Vigenere cipher"""
        valid, msg = self.validate_text(plaintext)
        if not valid:
            return None, msg

        valid, msg = self.validate_key(key)
        if not valid:
            return None, msg

        plaintext = self.prepare_text(plaintext)
        key = self.prepare_text(key)

        ciphertext = []
        key_length = len(key)

        for i, char in enumerate(plaintext):
            if char in self.char_to_num:
                plaintext_num = self.char_to_num[char]
                key_num = self.char_to_num[key[i % key_length]]
                encrypted_num = (plaintext_num + key_num) % self.alphabet_size
                ciphertext.append(self.num_to_char[encrypted_num])

        return "".join(ciphertext), ""

    def decrypt(self, ciphertext, key):
        """Decrypt message using Vigenere cipher"""
        valid, msg = self.validate_text(ciphertext)
        if not valid:
            return None, msg

        valid, msg = self.validate_key(key)
        if not valid:
            return None, msg

        ciphertext = self.prepare_text(ciphertext)
        key = self.prepare_text(key)

        plaintext = []
        key_length = len(key)

        for i, char in enumerate(ciphertext):
            if char in self.char_to_num:
                ciphertext_num = self.char_to_num[char]
                key_num = self.char_to_num[key[i % key_length]]
                decrypted_num = (ciphertext_num - key_num) % self.alphabet_size
                plaintext.append(self.num_to_char[decrypted_num])

        return "".join(plaintext), ""


def print_alphabet_table(cipher):
    """Display the alphabet with numeric codes"""
    print("\n" + "=" * 60)
    print("ROMANIAN ALPHABET WITH NUMERIC CODES:")
    print("=" * 60)

    for i in range(16):
        print(f"{cipher.alphabet[i]}:{i:2d}", end="  ")
    print()

    for i in range(16, 31):
        print(f"{cipher.alphabet[i]}:{i:2d}", end="  ")
    print("\n" + "=" * 60)


def main():
    cipher = VigenereCipher()

    print("=" * 60)
    print("VIGENERE CIPHER FOR ROMANIAN LANGUAGE")
    print("=" * 60)

    print_alphabet_table(cipher)

    while True:
        print("\nMENU:")
        print("1. Encrypt message")
        print("2. Decrypt message")
        print("3. Show alphabet")
        print("4. Exit")

        choice = input("\nChoose an option (1-4): ").strip()

        if choice == "1":
            print("\n--- ENCRYPTION ---")
            key = input("Enter the key (min. 7 characters): ")

            valid, msg = cipher.validate_key(key)
            if not valid:
                print(f"Error: {msg}")
                continue

            plaintext = input("Enter message to encrypt: ")

            ciphertext, error = cipher.encrypt(plaintext, key)
            if ciphertext:
                print(f"\nOriginal message: {plaintext}")
                print(f"Processed message: {cipher.prepare_text(plaintext)}")
                print(f"Used key: {cipher.prepare_text(key)}")
                print(f"Encrypted message: {ciphertext}")
            else:
                print(f"Error: {error}")

        elif choice == "2":
            print("\n--- DECRYPTION ---")
            key = input("Enter the key (min. 7 characters): ")

            valid, msg = cipher.validate_key(key)
            if not valid:
                print(f"Error: {msg}")
                continue

            ciphertext = input("Enter encrypted message: ")

            plaintext, error = cipher.decrypt(ciphertext, key)
            if plaintext:
                print(f"\nEncrypted message: {ciphertext}")
                print(f"Used key: {cipher.prepare_text(key)}")
                print(f"Decrypted message: {plaintext}")
            else:
                print(f"Error: {error}")

        elif choice == "3":
            print_alphabet_table(cipher)

        elif choice == "4":
            break

        else:
            print("Invalid option! Choose between 1 and 4.")


if __name__ == "__main__":
    print("USAGE EXAMPLE:")
    print("-" * 40)

    cipher = VigenereCipher()

    message = "Bună ziua România"
    key = "SECRETKEY"

    print(f"Original message: '{message}'")
    print(f"Key: '{key}'")

    text_encrypted, error = cipher.encrypt(message, key)
    if text_encrypted:
        print(f"Encrypted message: '{text_encrypted}'")

        text_decrypted, error = cipher.decrypt(text_encrypted, key)
        if text_decrypted:
            print(f"Decrypted message: '{text_decrypted}'")
    else:
        print(f"Encryption error: {error}")

    print("-" * 40)
    print("\nPress Enter to run the interactive program...")
    input()

    main()
