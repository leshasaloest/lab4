import random


def miller_rabin(n):
    if n <= 3:
        raise Exception('n should b greater than 3.')
    if n % 2 == 0:
        return False, 0
    u = n - 1
    k = 0
    while u % 2 == 0:
        u //= 2
        k += 1
    a = random.randint(2, n - 2)
    b = pow(a, u, n)
    if b == 1 or b == n - 1:
        return True, a
    for _ in range(1, k - 1):
        b = (b * b) % n
        if b == n - 1: return True, a
        if b == 1:
            return False, a
    return False, a


if __name__ == '__main__':
    for _ in range(100):
        n = random.randint(1, 100000000000)
        if miller_rabin(n)[0]:
            print(n, " is probably prime ", miller_rabin(n)[1])
        else:
            print(n, " not prime ", miller_rabin(n)[1])
