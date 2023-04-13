import sympy
import random
import math
import time


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def init_RSA(bit_size):
    bit_size_p = bit_size//2
    bit_size_q = bit_size-bit_size_p

    lower_range_p = 1 << (bit_size_p-1)
    upper_range_p = sum(1 << i for i in range(bit_size_p))
    p = sympy.randprime(lower_range_p, upper_range_p)

    lower_range_q = 1 << (bit_size_q-1)
    upper_range_q = sum(1 << i for i in range(bit_size_q))
    q = sympy.randprime(lower_range_q, upper_range_q)
    N = p*q
    phai = (p-1)*(q-1)
    e = random.randint(2, phai)
    temp = math.gcd(phai, e)
    while temp > 1:
        e = e//temp
        temp = math.gcd(phai, e)
    d = pow(e, -1, phai)
    return p, q, N, phai, e, d


def prime2_factorization(num):
    root = math.floor(math.sqrt(num))

    if root % 2 == 0:  # Only checks odd numbers, it reduces time by orders of magnitude
        root += 1
    if(num % 2 == 0):
        p = 2
        q = num//2
    else:
        p = 3
        while p <= root:
            if num % p == 0:
                break
            p += 2

    q = num//p
    return p, q


def attacker(e, N):
    p, q, phai, d = 0, 0, 0, 0
    p, q = prime2_factorization(N)
    phai = (p-1)*(q-1)
    d = pow(e, -1, phai)
    return p, q, phai, d


bit_size = int(
    input("Please enter the size of the publick key N in bits: "))
p, q, N, phai, e, d = init_RSA(bit_size)
print("the parameters of the RSA is:", flush=True)
print(f"p={p}, q={q}, N={N}, phai={phai}, e={e}, d={d}", flush=True)

# get the start time
st = time.time_ns()/1000000

temp_p, temp_q, temp_phai, temp_d = attacker(e, N)

# get the end time
et = time.time_ns()/1000000
if temp_p != p:
    temp_p, temp_q = temp_q, temp_p


# print(
#     f"temp_p={temp_p}, temp_q={temp_q}, temp_phai={temp_phai}, temp_d={temp_d}")
if((temp_p == p) and (temp_q == q) and (temp_phai == phai) and (temp_d == d)):
    print(f"{bcolors.BOLD}{bcolors.OKBLUE}Yes I could breake this ciphper eassy")
else:
    print(f"{bcolors.BOLD}{bcolors.FAIL}No I could not break this ciphper")
s = "{:,}".format(et-st)
print(f"{bcolors.BOLD}{bcolors.WARNING} the time needed to run the attak algorithm is: {s} milli seconds")
print(f"{bcolors.ENDC}-------------------------------------------------------")
