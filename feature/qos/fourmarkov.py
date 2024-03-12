import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

def cal_four_markov(data): #四状态马尔可夫
    # markov_num=[4][4]
    markov_num = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(1,len(data)):
        if data[i-1]<0.06:
            if data[i]<0.06:
                markov_num[0][0]=markov_num[0][0]+1
            elif data[i]<0.11:
                markov_num[0][1]=markov_num[0][1]+1
            elif data[i]<0.5:
                markov_num[0][2]=markov_num[0][2]+1
            else:
                markov_num[0][3] = markov_num[0][3] + 1
        elif data[i-1]<0.11:
            if data[i]<0.6:
                markov_num[1][0]=markov_num[1][0]+1
            elif data[i]<0.11:
                markov_num[1][1]=markov_num[1][1]+1
            elif data[i]<0.5:
                markov_num[1][2]=markov_num[1][2]+1
            else:
                markov_num[1][3] = markov_num[1][3] + 1
        elif data[i-1]<0.5:
            if data[i]<0.6:
                markov_num[2][0]=markov_num[2][0]+1
            elif data[i]<0.11:
                markov_num[2][1]=markov_num[2][1]+1
            elif data[i]<0.5:
                markov_num[2][2]=markov_num[2][2]+1
            else:
                markov_num[2][3] = markov_num[2][3] + 1
        else:
            if data[i]<0.6:
                markov_num[3][0]=markov_num[3][0]+1
            elif data[i]<0.11:
                markov_num[3][1]=markov_num[3][1]+1
            elif data[i]<0.5:
                markov_num[3][2]=markov_num[3][2]+1
            else:
                markov_num[3][3] = markov_num[3][3] + 1

    return markov_num

def cosine_similarity(matrix1, matrix2):   #余弦相似度
    dot_product = np.dot(matrix1.flatten(), matrix2.flatten())
    norm_matrix1 = np.linalg.norm(matrix1)
    norm_matrix2 = np.linalg.norm(matrix2)
    similarity = dot_product / (norm_matrix1 * norm_matrix2)
    return similarity

def pinghua(arr):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            arr[i][j] += 1
    return arr


