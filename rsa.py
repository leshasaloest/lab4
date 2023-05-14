import random


def generateKey(bits=1024):
    bits >>= 1
    e = 65537
    p = get_prime(bits)
    q = get_prime(bits)
    n = p * q
    eular = (p - 1) * (q - 1)
    x, y = get_(e, eular)
    d = x % eular
    return e, d, n


def endecrypt(x, e, c):
    return fastExpMod(x, e, c)


def fastExpMod(b, e, m):
    result = 1
    while e != 0:
        if (e & 1) == 1:
            result = (result * b) % m
        e >>= 1
        b = (b * b) % m
    return result


def get_prime(key_size=512):
    while True:
        num = random.randrange(2 ** (key_size - 1), 2 ** key_size)
        if is_prime(num):
            return num


def primeTest(n):
    q = n - 1
    k = 0
    while q % 2 == 0:
        k += 1
        q /= 2
    a = random.randint(2, n - 2)
    q = int(q)
    if fastExpMod(a, q, n) == 1:
        return True
    for j in range(0, k):
        if fastExpMod(a, (2 ** j) * q, n) == n - 1:
            return True
    return False


def rabin_miller(num):
    s = num - 1
    t = 0
    while s % 2 == 0:
        s = s // 2
        t += 1

    for trials in range(5):
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True


def is_prime(num):
    if num < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                    103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                    211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                    331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                    449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
                    587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                    709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
                    853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
                    991, 997]
    if num in small_primes:
        return True
    for prime in small_primes:
        if num % prime == 0:
            return False
    return rabin_miller(num)


def get_gcd(a, b):
    k = a // b
    remainder = a % b
    while remainder != 0:
        a = b
        b = remainder
        k = a // b
        remainder = a % b
    return b


def get_(a, b):
    if b == 0:
        return 1, 0
    else:
        k = a // b
        remainder = a % b
        x1, y1 = get_(b, remainder)
        x, y = y1, x1 - k * y1
    return x, y


def encrypt_raw(plaintext, n, e):
    if plaintext > n - 1:
        raise IndexError('You are trying to encrypt a message with invalid length.')
    return pow(plaintext, e, n)


def extended_gcd(a, b):
    if a[2] == 0:
        return b[1]
    else:
        q = b[2] // a[2]
        t1 = b[0] - q * a[0]
        t2 = b[1] - q * a[1]
        t3 = b[2] - q * a[2]
        return extended_gcd([t1, t2, t3], a)


def get_inv(num, mod):
    nums = [0, 1, num]
    mods = [1, 0, mod]
    return extended_gcd(nums, mods)


def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def get_mi(ls):
    m = 1
    result = []
    for pair in ls:
        m *= pair[0]
    for pair in ls:
        result.append([pair[0], m // pair[0]])
    return result, m


def get_ms_inv(ls):
    result = []
    for pair in ls:
        result.append(get_inv(pair[1], pair[0]))
    return result


def crt(ls):
    x = 0
    ms, m = get_mi(ls)
    es = get_ms_inv(ms)
    for i in range(len(ls)):
        x = (x + ms[i][1] * es[i] * ls[i][1]) % m
    return x


def decrypt_crt(ciphertext, p, q, d):
    cipher_p = ciphertext % p
    cipher_q = ciphertext % q
    d_p = d % (p - 1)
    d_q = d % (q - 1)
    x_p = pow(cipher_p, d_p, p)
    x_q = pow(cipher_q, d_q, q)
    return crt([[p, x_p], [q, x_q]])


if __name__ == '__main__':
    pass