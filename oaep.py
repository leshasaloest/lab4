import hashlib
import random
import rsa

K0 = K1 = 256
p = 0
q = 0
e = 65537
n = 0
eular = 0


def generateKey(bits=1024):
    global p, q, n, e, d, eular
    bits >>= 1
    e = 65537
    p = rsa.get_prime(bits)
    q = rsa.get_prime(bits)
    n = p * q
    eular = (p - 1) * (q - 1)
    x, y = rsa.get_(e, eular)
    d = x % eular
    return e, d, n


def encrypt(message, e, n):
    global K0, K1
    valueMessage = int(message, 16)
    r = random.randrange(1 << (K0 - 1), (1 << K0) - 1)
    keccak = hashlib.sha384(hex(r).encode('utf-8'))
    Gr = int(keccak.hexdigest(), 16)  # 384 bits
    X = (valueMessage << K1) ^ Gr
    keccak = hashlib.sha256(hex(X).encode('utf-8'))
    Hx = int(keccak.hexdigest(), 16)  # 256 bits
    Y = r ^ Hx
    res = (X << K0) + Y
    # RSA encryption
    encrypt = rsa.fastExpMod(res, e, n)
    return encrypt


def decrypt(encrypt, d, n):
    global K0, K1
    # RSA decryption
    encryptValue = rsa.fastExpMod(encrypt, d, n)

    Y = encryptValue % (1 << K0)
    X = encryptValue >> K0
    keccak = hashlib.sha256(hex(X).encode('utf-8'))
    Hx = int(keccak.hexdigest(), 16)  # 256 bits
    r = Y ^ Hx
    keccak = hashlib.sha384(hex(r).encode('utf-8'))
    Gr = int(keccak.hexdigest(), 16)  # 384 bits
    message = X ^ Gr
    message >>= K1
    return hex(message)


if __name__ == '__main__':
    a, b, c = generateKey()
    message = 0x592fa743889fc7f92ac2a37bb1f5ba1d
    encryptraw = rsa.encrypt_raw(message, n, e)
    print("Encrypted Message:", encryptraw)
    #
    encryptoaep = encrypt(hex(message), a, c)
    print("Encrypted Message:", encryptoaep)
    #
    decryptraw = rsa.decrypt_crt(encryptraw, p, q, d)
    print("Decrypted Message:", hex(decryptraw))
    #
    decryptoaep = decrypt(encryptoaep, b, c)
    print("Decrypted Message:", decryptoaep)
