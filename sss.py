#!/usr/bin/env python3

import argparse
from sss import shamir, io_reader

def main():
    parser = argparse.ArgumentParser(prog="sss",
                                     description="A simple Shamir's secret sharing program")

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-e",
        "--encrypt",
        action='store_false',
        help="Tells sss to encrypt a secret"
    )

    group.add_argument(
        "-d",
        "--decrypt",
        action='store_true',
        help="Tells sss to decrypt a secret"
    )

    parser.add_argument(
        "-t",
        "--threshold",
        metavar='threshold',
        type=int,
        required=True,
        help="Share threshold to recover the secret"
    )

    parser.add_argument(
        "-n",
        "--shares",
        metavar='shares',
        type=int,
        required=True,
        help="Number of shares to generate"
    )

    args = parser.parse_args()

    threshold = args.threshold
    shares = args.shares
    if args.decrypt:
        io_reader.print_secret(
            shamir.decrypt(io_reader.parse_shares(threshold), threshold, shares))
    else:
        io_reader.print_shares(
            shamir.encrypt(io_reader.parse_secret(threshold, shares), threshold, shares))

if __name__ == "__main__":
    main()
