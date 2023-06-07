from functools import wraps
import time

def timeit(func):
    @wraps(func)
    def timed(*args, **kw):
        ts = time.time()
        result = func(*args, **kw)
        te = time.time()

        print(f'func:{func.__name__} args:[{args}, {kw}] took: {te-ts} sec')
        return result
    return timed
