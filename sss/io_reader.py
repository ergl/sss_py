import sys

from . import shamir

def encode_secret(string):
    '''
    Encode a string as a bytebuffer, then as an integer
    '''
    return int.from_bytes(string.encode("ascii"), byteorder="big")

def decode_secret(num):
    '''
    Decode an integer into bytes, then into a string
    '''
    return num.to_bytes(((num.bit_length() + 7) // 8), byteorder="big").decode("ascii")

def parse_secret(threshold, total_shares):
    print('Generating shares using a ({},{}) scheme.'.format(threshold, total_shares))
    # The secret has to be smaller than the prime number
    # Since we're encoding the text as a number, with 8 bits per character,
    # we have to fit in the bit length of the chosen prime
    chosen_prime = shamir.PRIME
    prime_width = (chosen_prime.bit_length() // 8) - 1
    data_str = input('Enter the secret, at most {} ASCII characters: '.format(prime_width))
    if len(data_str) > prime_width:
        print("Error: Secret too large", file=sys.stderr)
        sys.exit(1)

    encoded = encode_secret(data_str)
    if encoded >= chosen_prime:
        print("Error: Secret too large", file=sys.stderr)
        sys.exit(1)

    return encoded

def parse_shares(threshold):
    print("Enter {} shares below:".format(threshold))
    shares = []
    for i in range(threshold):
        bare_share = input("Share [{}/{}]: ".format(i+1, threshold))
        matches = bare_share.split('-')
        if len(matches) != 2:
            print("Syntax Error: Bad share format")
            sys.exit(1)

        [x, y] = matches
        try:
            shares.append((int(x, 16), int(y, 16)))
        except ValueError:
            print("Syntax Error: Non-numeric share")
            sys.exit(1)

    return shares

def print_shares(shares):
    # Print as hex strings
    for x, y in shares:
        print("{:1x}-{:2x}".format(x,y))

def print_secret(secret):
    # Convert back to a string, then print it
    print("Resulting secret: {}".format(decode_secret(secret)))
