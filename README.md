# Shamir's Secret Sharing Scheme

A basic Shamir's Secret Sharing implementation, built for the Cryptography and Coding Theory course at UCM, 2019/2020.

You can find the Pony version in its [own repo](https://github.com/ergl/sss).

## Usage

Requires Python 3.6 or above.

```
$ python sss.py -h
usage: sss [-h] [-e | -d] -t threshold -n shares

A simple Shamir's secret sharing program

optional arguments:
  -h, --help            show this help message and exit
  -e, --encrypt         Tells sss to encrypt a secret
  -d, --decrypt         Tells sss to decrypt a secret
  -t threshold, --threshold threshold
                        Share threshold to recover the secret
  -n shares, --shares shares
                        Number of shares to generate
```
