from phe import paillier
import json
import numpy as np
import socket
from Toolkits import *
import secrets

np.random.seed(100)
M=100
S=100
truths=np.random.randint(low=0,high=10,size=M)
reliability=np.random.uniform(0,5,S)
data=np.zeros((S,M))
for i in range():
    data[i]=truths+np.random.normal(0,reliability[i],M)



def key_exchange_P1(pk, s):
    pk_dict = {'n': pk.n}
    msg = bytes(json.dumps(pk_dict), encoding='utf-8')
    s.send(msg)


if __name__ == "__main__":
    # key generation
    pk, sk = paillier.generate_paillier_keypair()
    secrets = np.random.normal(0, 0.5, 10)

    # socket
    s = socket.socket()
    host = socket.gethostname()
    port = 8888 
    s.connect((host, port))

    # key exchange
    key_exchange_P1(pk, s)

    # encrypt secrets
    encrypted_secrets=pk.encrypt(secrets)
    msg=serialize(encrypted_secrets)
    s.send(msg)

    # waiting for response
