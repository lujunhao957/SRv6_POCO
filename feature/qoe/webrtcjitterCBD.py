import math
import numpy

def g(t: float, a: float, b: float, m: int) -> float:
    factor = m/math.sqrt(2*math.pi*a*pow(t, 3))
    factor2 = math.exp(-pow(m+b*t, 2)/(2*a*t))
    return factor*factor2

def get_jitter_CBD(avg,std,resolution,fps,CBD):
    lambda_ = 1.0 / avg
    mu = 0.26
    alpha = pow(lambda_, 3) * std
    beta = lambda_ - mu
    G1 = 0.0
    g_list = []
    G_list = []
    x = [round(t, 1) for t in list(numpy.arange(1.0, 350.0, 1))]
    for i in x:
        cur_g = g(i, alpha, beta, 7)
        G1 = G1 + cur_g
        g_list.append(cur_g)
        G_list.append(G1)

    cur_G = 0.0
    for i in g_list:
        cur_G = cur_G + i

    xx = []
    gl = []

    for i in range(20, len(x)):
        xx.append(x[i])

    for i in range(0, len(xx)):
        gl.append(G_list[i])

    res=0
    print(xx)
    print(gl)
    for i in range(1,len(xx)-2):
        if xx[i-1]<=CBD and xx[i+1]>=CBD:
            res=gl[i]
            break
    return res

# if __name__ == '__main__':
#     count=get_jitter_CBD(5.019130777676027,1.45512817435018232,1080,25,150)
#     print(count)


