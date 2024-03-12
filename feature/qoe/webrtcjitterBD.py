import math
import numpy

def g(t: int, a: float, b: float, m: int) -> float:
    factor = m/math.sqrt(2*math.pi*a*pow(t, 3))
    factor2 = math.exp(-pow(m-b*t, 2)/(2*a*t))
    return factor*factor2

def get_jitter_BD(avg,std,resolution,fps,BD):
    # print(avg, var, std)
    lambda_ = 1.0 / avg
    mu = 0.033
    alpha = pow(lambda_, 3) * std
    beta = lambda_ - mu
    G1 = 0.0
    G2 = 0.0
    g_list = []
    G_list = []
    G_list_nihe = []
    G_list_real = []
    # x = range(1, 100)
    # 1-350, 0.1 step
    x = [round(t, 1) for t in list(numpy.arange(1.0, 100.0, 0.1))]
    for j in x:
        cur_g = g(j, alpha, beta, 7)
        G1 = G1 + cur_g
        g_list.append(cur_g)
        G_list.append(G1)
    G_list = [j / 10 for j in G_list]

    cur_G = 0.0

    for j in g_list:
        cur_G = cur_G + j
        G_list_real.append(cur_G)

    xx = []
    gl = []

    for j in range(200, len(x)):
        xx.append(x[j])
        gl.append(G_list[j])
    print(xx)
    print(gl)
    res=0
    for i in range(1,len(xx)-2):
        if xx[i-1]<=BD and xx[i+1]>=BD:
            res=gl[i]
            break
    return res

# if __name__ == '__main__':
#     count=get_jitter_BD(4.999130777676027,3.45512817435018232,1080,25,50)
#     print(count)


