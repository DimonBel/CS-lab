"""
Main file to run both RSA and ElGamal digital signature implementations
Laboratory Work #6
"""


def main():
    print("Laboratory Work #6: Hash Functions and Digital Signatures")
    print("=" * 60)
    print()

    # Import and run RSA signature
    try:
        from rsa_signature import rsa_sign_and_verify

        print("Task 1: RSA Digital Signature with MD2")
        success_rsa = rsa_sign_and_verify()
        print()
    except ImportError as e:
        print(f"Error importing RSA module: {e}")
        success_rsa = False
    except Exception as e:
        print(f"Error in RSA implementation: {e}")
        success_rsa = False

    print("\n" + "-" * 60 + "\n")

    # Import and run ElGamal signature
    try:
        from elgamal_signature import elgamal_sign_and_verify

        print("Task 2: ElGamal Digital Signature with MD5")
        success_elgamal = elgamal_sign_and_verify()
        print()
    except ImportError as e:
        print(f"Error importing ElGamal module: {e}")
        success_elgamal = False
    except Exception as e:
        print(f"Error in ElGamal implementation: {e}")
        success_elgamal = False

    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"RSA Signature: {'SUCCESS' if success_rsa else 'FAILED'}")
    print(f"ElGamal Signature: {'SUCCESS' if success_elgamal else 'FAILED'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
