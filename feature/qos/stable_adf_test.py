import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller

df = pd.read_excel('D:/webrtcdata/TXDJTXBJ/rtt.xlsx', sheet_name='Sheet1', usecols='A:B')
data = df.values
datat=[]
for i in range(1,10000):
    datat.append(data[i][1]/1000)

rtt_result=adfuller(datat)         # 生成adf检验结果

print('The ADF Statistic of interval: %f' % rtt_result[0])         # adf值,越负越能拒绝原假设
print('The p value of interval: %f' % rtt_result[1])               # p值,以常用的判断标准值0.05作为参考,小于0.05则为平稳的
