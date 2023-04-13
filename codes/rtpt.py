import shamir
import Crypto

if __name__ == "__main__":
    max=2**31-1
    secret=1231324
    shares=shamir.make_random_shares(7,10,secret,max)
    print(shares)
    print(secret)
    print(shamir.recover_secret(shares[2:9],max))