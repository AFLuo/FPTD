
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
x=np.array(list(range(10,300)))
coeff=[ 4.12993220e-11, -1.15721125e-09,  1.76707773e-07,  4.87822439e-05,-8.16406290e-04]
plt.plot(x,coeff[0]*(x**4)+coeff[1]*(x**3)+coeff[2]*(x**2)+coeff[3]*x+coeff[4],'k-')
plt.show()