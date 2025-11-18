from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import time
import os
import matplotlib.pyplot as plt

# test message
message = b"This is a test message for cryptography"


def pad(data, block_size=16):
    padding_len = block_size - (len(data) % block_size)
    return data + bytes([padding_len]) * padding_len


def unpad(data):
    if not data:
        return data
    padding_len = data[-1]
    if padding_len < 1 or padding_len > 16:
        raise ValueError("Invalid padding")
    return data[:-padding_len]


def generate_keys():
    """Generate AES (128 & 256) keys and RSA key pair and save to files."""
    # AES keys
    aes_128_key = get_random_bytes(16)
    aes_256_key = get_random_bytes(32)

    with open('aes_128.key', 'wb') as f:
        f.write(aes_128_key)

    with open('aes_256.key', 'wb') as f:
        f.write(aes_256_key)

    # RSA keys
    rsa_key = RSA.generate(2048)

    with open('rsa_private.pem', 'wb') as f:
        f.write(rsa_key.export_key())

    with open('rsa_public.pem', 'wb') as f:
        f.write(rsa_key.publickey().export_key())

    print("Keys generated and saved")


def aes_ecb_encrypt(key_size):
    print(f"\nAES-{key_size} ECB Encryption")

    with open(f'aes_{key_size}.key', 'rb') as keyfile:
        key = keyfile.read()

    start = time.time()
    cipher = AES.new(key, AES.MODE_ECB)

    padded_msg = pad(message, AES.block_size)

    ciphertext = cipher.encrypt(padded_msg)
    end = time.time()

    with open(f'encrypted_ecb_{key_size}.bin', 'wb') as outfile:
        outfile.write(ciphertext)

    print(f"Encrypted saved to: encrypted_ecb_{key_size}.bin")
    print(f"Time: {end - start:.6f} seconds")
    return end - start


def aes_ecb_decrypt(key_size):
    print(f"\nAES-{key_size} ECB Decryption")

    with open(f'aes_{key_size}.key', 'rb') as keyfile:
        key = keyfile.read()

    with open(f'encrypted_ecb_{key_size}.bin', 'rb') as infile:
        ciphertext = infile.read()

    start = time.time()
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)

    # remove padding
    try:
        decrypted = unpad(decrypted)
    except ValueError as e:
        print('Warning: unpadding failed:', e)
    end = time.time()

    try:
        print(f"Decrypted: {decrypted.decode()}")
    except Exception:
        print("Decrypted (raw bytes):", decrypted)

    print(f"Time: {end - start:.6f} seconds")
    return end - start


def aes_cfb_encrypt(key_size):
    print(f"\nAES-{key_size} CFB Encryption")

    with open(f'aes_{key_size}.key', 'rb') as keyfile:
        key = keyfile.read()

    start = time.time()
    iv = get_random_bytes(16)
    # use full-block feedback for simplicity
    cipher = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128)
    ciphertext = cipher.encrypt(message)
    end = time.time()

    with open(f'encrypted_cfb_{key_size}.bin', 'wb') as outfile:
        outfile.write(iv + ciphertext)

    print(f"Encrypted saved to: encrypted_cfb_{key_size}.bin")
    print(f"Time: {end - start:.6f} seconds")
    return end - start


def aes_cfb_decrypt(key_size):
    print(f"\nAES-{key_size} CFB Decryption")

    with open(f'aes_{key_size}.key', 'rb') as keyfile:
        key = keyfile.read()

    with open(f'encrypted_cfb_{key_size}.bin', 'rb') as infile:
        data = infile.read()

    iv = data[:16]
    ciphertext = data[16:]

    start = time.time()
    cipher = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128)
    decrypted = cipher.decrypt(ciphertext)
    end = time.time()

    try:
        print(f"Decrypted: {decrypted.decode()}")
    except Exception:
        print("Decrypted (raw bytes):", decrypted)

    print(f"Time: {end - start:.6f} seconds")
    return end - start


def rsa_encrypt():
    print("\nRSA Encryption")

    with open('rsa_public.pem', 'rb') as keyfile:
        public_key = RSA.import_key(keyfile.read())

    start = time.time()
    cipher = PKCS1_OAEP.new(public_key)
    ciphertext = cipher.encrypt(message)
    end = time.time()

    with open('encrypted_rsa.bin', 'wb') as outfile:
        outfile.write(ciphertext)

    print("Encrypted saved to: encrypted_rsa.bin")
    print(f"Time: {end - start:.6f} seconds")
    return end - start


def rsa_decrypt():
    print("\nRSA Decryption")

    with open('rsa_private.pem', 'rb') as keyfile:
        private_key = RSA.import_key(keyfile.read())

    with open('encrypted_rsa.bin', 'rb') as infile:
        ciphertext = infile.read()

    start = time.time()
    cipher = PKCS1_OAEP.new(private_key)
    decrypted = cipher.decrypt(ciphertext)
    end = time.time()

    print(f"Decrypted: {decrypted.decode()}")
    print(f"Time: {end - start:.6f} seconds")
    return end - start


def rsa_sign():
    print("\nRSA Signature")

    with open('rsa_private.pem', 'rb') as keyfile:
        private_key = RSA.import_key(keyfile.read())

    start = time.time()
    h = SHA256.new(message)
    signature = pkcs1_15.new(private_key).sign(h)
    end = time.time()

    with open('message.txt', 'wb') as msgfile:
        msgfile.write(message)

    with open('signature.sig', 'wb') as sigfile:
        sigfile.write(signature)

    print("Message saved to: message.txt")
    print("Signature saved to: signature.sig")
    print(f"Time: {end - start:.6f} seconds")
    return end - start


def rsa_verify():
    print("\nRSA Signature Verification")

    with open('rsa_public.pem', 'rb') as keyfile:
        public_key = RSA.import_key(keyfile.read())

    with open('message.txt', 'rb') as msgfile:
        msg = msgfile.read()

    with open('signature.sig', 'rb') as sigfile:
        signature = sigfile.read()

    start = time.time()
    h = SHA256.new(msg)
    try:
        pkcs1_15.new(public_key).verify(h, signature)
        print("Signature is VALID")
    except (ValueError, TypeError):
        print("Signature is INVALID")
    end = time.time()

    print(f"Time: {end - start:.6f} seconds")
    return end - start


def sha256_hash():
    print("\nSHA-256 Hashing")

    start = time.time()
    h = SHA256.new(message)
    hash_value = h.hexdigest()
    end = time.time()

    print(f"Message: {message.decode()}")
    print(f"SHA-256: {hash_value}")
    print(f"Time: {end - start:.6f} seconds")
    return end - start


def performance_test():
    print("\nPerformance Testing")
    print("Testing with different key sizes\n")

    # AES performance - 3 standard sizes
    print("Testing AES encryption:")
    aes_key_sizes_bits = [128, 192, 256]
    aes_times = []

    for bits in aes_key_sizes_bits:
        if bits == 128:
            key = get_random_bytes(16)
        elif bits == 192:
            key = get_random_bytes(24)
        else:
            key = get_random_bytes(32)

        start = time.time()
        cipher = AES.new(key, AES.MODE_ECB)
        padded = pad(message, AES.block_size)
        cipher.encrypt(padded)
        end = time.time()

        elapsed = end - start
        aes_times.append(elapsed)
        print(f"AES-{bits} bits: {elapsed:.6f} seconds")

    # RSA performance - 4 sizes (all >= 1024 bits)
    print("\nTesting RSA key generation:")
    rsa_key_sizes = [1024, 1536, 2048, 3072]
    rsa_times = []

    print(f"RSA key sizes to test: {rsa_key_sizes}")
    for size in rsa_key_sizes:
        print(f"  Generating RSA-{size} bits...", end=' ')
        try:
            start = time.time()
            key = RSA.generate(size)
            end = time.time()
            print(f"{end - start:.6f} seconds (key size verified: {key.size_in_bits()} bits)")
        except Exception as e:
            print(f"\nError generating {size}-bit key: {str(e)}")
            end = time.time()

        elapsed = end - start
        rsa_times.append(elapsed)
        print(f"{elapsed:.6f} seconds")

    # Create performance graphs
    print("\nGenerating graphs - ")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # AES graph
    ax1.plot(aes_key_sizes_bits, aes_times, marker='o', color='blue', linewidth=2)
    ax1.set_xlabel('Key Size (bits)')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_title('AES Encryption Performance')
    ax1.grid(True)

    # RSA graph
    ax2.plot(rsa_key_sizes, rsa_times, marker='s', color='red', linewidth=2)
    ax2.set_xlabel('Key Size (bits)')
    ax2.set_ylabel('Time (seconds)')
    ax2.set_title('RSA Key Generation Performance')
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig('performance_graph.png')
    print("Graph saved: performance_graph.png")
    print("Performance testing completed")


def main():
    print("Cryptography Lab Program")

    if not os.path.exists('aes_128.key') or not os.path.exists('rsa_private.pem'):
        generate_keys()

    while True:
        print("\n" + "-" * 50)
        print("Menu:")
        print("1. AES-128 ECB")
        print("2. AES-256 ECB")
        print("3. AES-128 CFB")
        print("4. AES-256 CFB")
        print("5. RSA Encryption/Decryption")
        print("6. RSA Signature")
        print("7. SHA-256 Hash")
        print("8. Performance Test")
        print("0. Exit")
        print("-" * 50)

        choice = input("Choose option: ")

        if choice == '1':
            aes_ecb_encrypt(128)
            aes_ecb_decrypt(128)
        elif choice == '2':
            aes_ecb_encrypt(256)
            aes_ecb_decrypt(256)
        elif choice == '3':
            aes_cfb_encrypt(128)
            aes_cfb_decrypt(128)
        elif choice == '4':
            aes_cfb_encrypt(256)
            aes_cfb_decrypt(256)
        elif choice == '5':
            rsa_encrypt()
            rsa_decrypt()
        elif choice == '6':
            rsa_sign()
            rsa_verify()
        elif choice == '7':
            sha256_hash()
        elif choice == '8':
            performance_test()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
