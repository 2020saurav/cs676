import math

def g_flat(x):
    if x < 1:
        return 1
    else:
        return 0

def sq_norm(x):
    result=0
    for i in range(0, len(x)):
        result+= x[i]*x[i]
    return result

def epan_kernel(x):
    if x >= 0 and x <= 1:
        return 1 - x
    else:
        return 0

def gaussian_kernel(x):
    #x is squared norm
    return math.exp(-0.5*x)


def difference(x, y):
    z = []
    for i in range(0, len(x)):
        z.append(float(x[i]) - float(y[i]))
    return z

def multiply(x, c):
    z = []
    for i in range(0, len(x)):
        z.append(x[i] * c)
    return z

def add(x, y):
    z = []
    for i in range(0, len(x)):
        z.append(x[i] + y[i])
    return z
