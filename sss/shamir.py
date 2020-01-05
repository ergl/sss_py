import secrets

# A 80-digit prime number, large enough to fit a 32-digit ASCII string inside
PRIME=18532395500947174450709383384936679868383424444311405679463280782405796233163977

def encrypt(secret, threshold, total_shares):
    # First, generate t random numbers, with the secret at poly(0)
    poly = [secrets.randbelow(PRIME) for t in range(threshold)]
    poly[0] = secret

    # Next, we evaluate the polynomial at x \in {1..t}
    # (skip x=0, as that is secret)
    shares = [
        (x, _evaluate(poly, x, PRIME))
            for x in range(total_shares + 1)
    ]

    # Skip the secret
    return shares[1:]

def _evaluate(poly, x, prime):
    res = 0
    for coeff in reversed(poly):
        res = (res * x) % prime
        res = (res + coeff) % prime
    return res

def decrypt(shares, threshold, total_shares):
    if len(shares) == 1:
        # If there's one share, then shares[0] == secret
        return None

    return _interpolate(shares, PRIME)

def _interpolate(shares, prime):
    secret = 0
    for x_j, y_j in shares:
        l_j = _lagrange_poly_at(x_j, shares, prime)
        secret = (secret + ((y_j * l_j) % prime)) % prime
    return secret

def _lagrange_poly_at(x_j, xs, prime):
    acc = 1
    for x, _ in xs:
        if x != x_j:
            dem = (x - x_j) % prime
            div = _div_mod(x, dem, prime)
            acc = (acc * div) % prime
    return acc

# Since (n / m) is n * 1/m, (n / m) mod p is n * m^-1 mod p
def _div_mod(n, m, prime):
    return (n * _inverse(m, prime)) % prime

# Implementation taken from
# https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Modular_integers
def _inverse(m, p):
    (t, new_t) = (0, 1)
    (r, new_r) = (p, m)
    while new_r != 0:
        quot = r // new_r
        (t, new_t) = (new_t, t - (quot * new_t))
        (r, new_r) = (new_r, r - (quot * new_r))

    if t < 0:
        t += p

    return t % p
