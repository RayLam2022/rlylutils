import time
import numba
from numba import cuda
from functools import wraps


def timeit(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        enter_time = time.time()
        ret = f(*args, **kwargs)
        print("{}:{}".format(f.__name__, time.time()-enter_time))
        return ret
    return wrapper


@timeit
def fib(n):
    f1 = f2 = 1
    for i in range(1, n):
        f1, f2 = f2, f1 + f2
    return f2


@timeit
@numba.jit
def fib_with_jit(n):
    f1 = f2 = 1
    for i in range(1, n):
        f1, f2 = f2, f1 + f2
    return f2


import numpy as np
from timeit import default_timer as timer
from numba import vectorize

@vectorize(['float32(float32, float32)'], target='cuda')
def vector_add(a, b):
    return a + b


def main():
    n = 3200000

    a = np.ones(n, dtype=np.float32)
    b = np.ones(n, dtype=np.float32)
    # c = np.ones(n, dtype=np.float32)

    start = timer()
    c = vector_add(a, b)
    vector_add_time = timer() - start

    print(c[:5])
    print(c[-5:])
    print(vector_add_time)



main()
#fib_with_cudajit(2000000)
fib_with_jit(2000000)	# fib_with_jit:0.11314105987548828
fib(2000000)	# fib:50.43636465072632