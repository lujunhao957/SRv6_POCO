import numpy
import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# 定义一个空的二维数组
n_dimensional_array = []

# 定义要添加的一维数组
one_dimensional_array1 = np.random.normal(0, 3, size=60000)
one_dimensional_array2 = np.random.normal(0, 6, size=60000)
one_dimensional_array3 = np.random.normal(0, 10, size=60000)
# 将一维数组添加到二维数组中
n_dimensional_array.append(one_dimensional_array1)
n_dimensional_array.append(one_dimensional_array2)
n_dimensional_array.append(one_dimensional_array3)

x_dimensional_array = []
y_dimensional_array = []
logy_dimensional_array = []
gradient_dimensional_array = []

# Define the Hamiltonian function
def H(x, v):
    # U = 0.5 * np.dot(np.dot((x - mu).T, Sigma_inv), (x - mu)) # potential energy
    length=len(x)
    U=0
    for i in range(0, length):
        if x[i] < x_dimensional_array[i][0]:
            U=U-logy_dimensional_array[i][0]
        elif x[i] > x_dimensional_array[i][len(x_dimensional_array[i]) - 1]:
            U=U-logy_dimensional_array[i][len(logy_dimensional_array[i]) - 1]
        else:
            t = (x[i] - x_dimensional_array[i][0]) / (
                        x_dimensional_array[i][len(x_dimensional_array[i]) - 1] - x_dimensional_array[i][0]) * len(
                x_dimensional_array[i])
            U=U-logy_dimensional_array[i][int(t)]
    K = 0.5 * np.dot(v.T, v) # kinetic energy
    return U + K

# Define the gradient of the potential energy
def grad_U(x):
    length=len(x)
    res = []
    for i in range(0,length):
        if x[i]<x_dimensional_array[i][0]:
            res.append(gradient_dimensional_array[i][0])
        elif x[i]>x_dimensional_array[i][len(x_dimensional_array[i])-1]:
            res.append(gradient_dimensional_array[i][len(gradient_dimensional_array[i])-1])
        else:
            t = (x[i] - x_dimensional_array[i][0])/ (x_dimensional_array[i][len(x_dimensional_array[i])-1]- x_dimensional_array[i][0]) * len(x_dimensional_array[i])
            res.append(gradient_dimensional_array[i][int(t)])
    return np.array(res)
    # return np.dot(Sigma_inv, (x - mu))

# Define the Leapfrog method
def Leapfrog(x, v, epsilon, L):
    v_half = v - 0.5 * epsilon * grad_U(x) # half step update for velocity
    for i in range(L):
        x = x + epsilon * v_half # full step update for position
        if i != L - 1:
            v_half = v_half - epsilon * grad_U(x) # full step update for velocity
    v = v_half - 0.5 * epsilon * grad_U(x) # half step update for velocity
    return x, v

# Define the HMC algorithm
def HMC(x_init, epsilon, L, N):
    x = x_init # initial position
    samples = [] # list of samples
    accept_count = 0 # number of accepted proposals
    for i in range(N):
        v = np.random.randn(len(x)) # sample velocity from standard normal
        x_star, v_star = Leapfrog(x, v, epsilon, L) # propose new state using Leapfrog
        alpha = np.exp(H(x, v) - H(x_star, v_star)) # acceptance probability
        u = np.random.rand() # sample a uniform random number
        if u < alpha: # accept the proposal
            x = x_star
            accept_count += 1
        samples.append(x) # store the sample
    accept_rate = accept_count / N # acceptance rate
    return np.array(samples), accept_rate

def drawn_dimensional_array():
    # Set the parameters
    x_init = np.array([1, 1, 1]) # initial position
    epsilon = 0.1 # step size
    L = 10 # number of steps
    N = 10000 # number of samples

    # Run the HMC algorithm
    samples, accept_rate = HMC(x_init, epsilon, L, N)
    count=0

    fenbu=[]

    for i in range(0,len(samples)):
        count=samples[i][0]+count
        fenbu.append(samples[i][0]+samples[i][1]+samples[i][2])
    print("Acceptance rate:", accept_rate)
    res=np.array(fenbu)
    mean_value = np.mean(res)
    standard_deviation = np.std(res)
    print("mean:",mean_value)
    print("standard_deviation:", standard_deviation)
    # print(res)

def initial_data():
    for i in range(0,len(n_dimensional_array)):
        ax = sns.kdeplot(n_dimensional_array[i])
        x, y = ax.get_lines()[i].get_data()
        x_dimensional_array.append(np.array(x))
        y_dimensional_array.append(np.array(y))
        a = np.array(y)
        b = numpy.log(a)
        logy_dimensional_array.append(np.array(b))
        gra = np.gradient(b)
        gradient_dimensional_array.append(np.array(gra))
    # print(gradient_dimensional_array)

if __name__ == '__main__':
    initial_data()
    drawn_dimensional_array()