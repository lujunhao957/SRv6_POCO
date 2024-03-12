import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency


def cal_four_markov(data):
    markov_num = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(1, len(data)):
        if data[i - 1] < 0.06:
            if data[i] < 0.06:
                markov_num[0][0] = markov_num[0][0] + 1
            elif data[i] < 0.11:
                markov_num[0][1] = markov_num[0][1] + 1
            elif data[i] < 0.5:
                markov_num[0][2] = markov_num[0][2] + 1
            else:
                markov_num[0][3] = markov_num[0][3] + 1
        elif data[i - 1] < 0.11:
            if data[i] < 0.6:
                markov_num[1][0] = markov_num[1][0] + 1
            elif data[i] < 0.11:
                markov_num[1][1] = markov_num[1][1] + 1
            elif data[i] < 0.5:
                markov_num[1][2] = markov_num[1][2] + 1
            else:
                markov_num[1][3] = markov_num[1][3] + 1
        elif data[i - 1] < 0.5:
            if data[i] < 0.6:
                markov_num[2][0] = markov_num[2][0] + 1
            elif data[i] < 0.11:
                markov_num[2][1] = markov_num[2][1] + 1
            elif data[i] < 0.5:
                markov_num[2][2] = markov_num[2][2] + 1
            else:
                markov_num[2][3] = markov_num[2][3] + 1
        else:
            if data[i] < 0.6:
                markov_num[3][0] = markov_num[3][0] + 1
            elif data[i] < 0.11:
                markov_num[3][1] = markov_num[3][1] + 1
            elif data[i] < 0.5:
                markov_num[3][2] = markov_num[3][2] + 1
            else:
                markov_num[3][3] = markov_num[3][3] + 1
    return markov_num


def get_loss_BD(data, rtt):
    res = []
    p1 = data[6][0] * (1 - data[0][0]) + data[6][1] * (data[1][2] + data[1][3] + data[1][4] + data[1][5]) + data[6][
        2] * (data[2][3] + data[2][4] + data[2][5]) + data[6][3] * (data[3][4] + data[3][5]) + data[6][4] * data[4][5] + \
         data[6][5] * data[5][5]
    p2 = data[6][0] * data[0][1] * (data[1][2] + data[2][3] + data[3][4] + data[4][5]) + data[6][0] * data[0][2] * (
                data[2][3] + data[2][4] + data[2][5]) + data[6][0] * data[0][3] * (data[3][4] + data[3][5]) + data[6][
             0] * data[0][4] * data[4][5] + data[6][0] * data[0][5] * data[5][5] + data[6][1] * data[1][2] * (
                     data[2][3] + data[2][4] + data[2][5])
    p3 = 0.1 * p2
    p4 = 0.08 * p3
    res.append(p1)
    res.append(p2)
    res.append(p3)
    res.append(p4)
    res.append(p4 * 0.1)
    x = []
    y = []
    m = []
    n = []
    x.append(0)
    y.append(0)
    m.append(0)
    n.append(0)
    temp = 1 - p1
    ans = temp
    t = 1
    for j in range(1, 800):
        if (j > 600):
            temp = 1
            ans = 1
        elif (j % rtt == 0):
            if t >= len(res):
                temp = 1
            else:
                temp = 1 - res[t]
            t = t + 1
            if temp >= ans:
                ans = temp
            else:
                if (ans * 1.03 < 1):
                    ans = ans * 1.03
                else:
                    ans = 1
        x.append(j)
        y.append(temp)
        if len(m) > 1:
            if m[len(m) - 1] > j:
                continue
        m.append(j)
        n.append(ans)
    last = n[0]
    for j in range(1, 800):
        if (n[j] < n[j - 1]):
            n[j] = n[j - 1]
