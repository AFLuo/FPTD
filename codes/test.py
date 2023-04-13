
from binascii import hexlify,unhexlify
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.SecretSharing import Shamir
import shamir
import time
import math
import matplotlib.pyplot as plt
import numpy as np
from numpy import polyfit, poly1d
from scipy.linalg import lstsq
from scipy.stats import linregress


share_time=[]
recover_time=[]
for n in range(10,300):
    t=math.ceil(3*n/4)
    start=time.time()
    shares=shamir.make_random_shares(t,n,588,2**128-1)
    end=time.time()
    share_time.append(end-start)

    start=time.time()
    s2=shamir.recover_secret(shares[:t+1],2**128-1)
    end=time.time()
    recover_time.append(end-start)

x=np.array(list(range(10,300)))
plt.plot(x,share_time,color='red')
plt.plot(x,recover_time,color='blue')
coeff=polyfit(x,recover_time,4)
plt.plot(x,coeff[0]*(x**4)+coeff[1]*(x**3)+coeff[2]*(x**2)+coeff[3]*x+coeff[4],'k-')
print(coeff)
plt.show()