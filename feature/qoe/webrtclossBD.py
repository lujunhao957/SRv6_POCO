from sympy import symbols, solve, linsolve, Eq

def cal_markov_stable_probability(data):
    p1,p2,p3,p4,p5,p6,p7 = symbols('p1 p2 p3 p4 p5 p6 p7')
    temp = 0
    for i in range(0, 7):
        for j in range(0, 7):
            if data[i][j] != 0:
                temp = i
    temp = temp + 1
    if temp == 1:
        return 1
    elif temp == 2:
        f1 = Eq(p1 * (data[0][0]) + p2 * data[1][0], p1)
        f2 = Eq(p1 * data[0][1] + p2 * (data[1][1]), p2)
        f5 = Eq(p1 + p2, 1)
        solutions = solve((f1, f5), (p1, p2))
        print(solutions)
    elif temp == 3:
        f1 = Eq(p1 * (data[0][0]) + p2 * data[1][0] + p3 * data[2][0], p1)
        f2 = Eq(p1 * data[0][1] + p2 * (data[1][1]) + p3 * data[2][1], p2)
        f3 = Eq(p1 * data[0][2] + p2 * data[1][2] + p3 * (data[2][2]), p3)
        f5 = Eq(p1 + p2 + p3, 1)
        solutions = solve((f1, f2, f5), (p1, p2, p3))
        print(solutions)
    elif temp == 4:
        f1 = Eq(p1 * (data[0][0]) + p2 * data[1][0] + p3 * data[2][0] + p4 * data[3][0], p1)
        f2 = Eq(p1 * data[0][1] + p2 * (data[1][1]) + p3 * data[2][1] + p4 * data[3][1], p2)
        f3 = Eq(p1 * data[0][2] + p2 * data[1][2] + p3 * (data[2][2]) + p4 * data[3][2], p3)
        f4 = Eq(p1 * data[0][3] + p2 * data[1][3] + p3 * data[2][3] + p4 * (data[3][3]), p4)
        f5 = Eq(p1 + p2 + p3 + p4, 1)
        solutions = solve((f1, f2, f3, f5), (p1, p2, p3, p4))
        print(solutions)
    elif temp == 5:
        f1 = Eq(p1 * (data[0][0]) + p2 * data[1][0] + p3 * data[2][0] + p4 * data[3][0] + p5 * data[4][0], p1)
        f2 = Eq(p1 * data[0][1] + p2 * (data[1][1]) + p3 * data[2][1] + p4 * data[3][1] + p5 * data[4][1], p2)
        f3 = Eq(p1 * data[0][2] + p2 * data[1][2] + p3 * (data[2][2]) + p4 * data[3][2] + p5 * data[4][2], p3)
        f4 = Eq(p1 * data[0][3] + p2 * data[1][3] + p3 * data[2][3] + p4 * (data[3][3]) + p5 * data[4][3], p4)
        f5 = Eq(p1 * data[0][4] + p2 * data[1][4] + p3 * data[2][4] + p4 * data[3][4] + p5 * (data[4][4]), p5)
        f7 = Eq(p1 + p2 + p3 + p4 + p5, 1)
        solutions = solve((f1, f2, f3, f4, f7), (p1, p2, p3, p4, p5))
        print(solutions)
    elif temp == 6:
        f1 = Eq(
            p1 * (data[0][0]) + p2 * data[1][0] + p3 * data[2][0] + p4 * data[3][0] + p5 * data[4][0] + p6 * data[5][0],
            p1)
        f2 = Eq(
            p1 * data[0][1] + p2 * (data[1][1]) + p3 * data[2][1] + p4 * data[3][1] + p5 * data[4][1] + p6 * data[5][1],
            p2)
        f3 = Eq(
            p1 * data[0][2] + p2 * data[1][2] + p3 * (data[2][2]) + p4 * data[3][2] + p5 * data[4][2] + p6 * data[5][2],
            p3)
        f4 = Eq(
            p1 * data[0][3] + p2 * data[1][3] + p3 * data[2][3] + p4 * (data[3][3]) + p5 * data[4][3] + p6 * data[5][3],
            p4)
        f5 = Eq(
            p1 * data[0][4] + p2 * data[1][4] + p3 * data[2][4] + p4 * data[3][4] + p5 * (data[4][4]) + p6 * data[5][4],
            p5)
        f6 = Eq(
            p1 * data[0][5] + p2 * data[1][5] + p3 * data[2][5] + p4 * data[3][5] + p5 * data[4][5] + p6 * (data[5][5]),
            p6)
        f7 = Eq(p1 + p2 + p3 + p4 + p5 + p6, 1)
        solutions = solve((f1, f2, f3, f4, f5, f7), (p1, p2, p3, p4, p5, p6))
        print(solutions)
    elif temp == 7:
        f1 = Eq(
            p1 * (data[0][0]) + p2 * data[1][0] + p3 * data[2][0] + p4 * data[3][0] + p5 * data[4][0] + p6 * data[5][0] + p7 * data[6][0],
            p1)
        f2 = Eq(
            p1 * data[0][1] + p2 * (data[1][1]) + p3 * data[2][1] + p4 * data[3][1] + p5 * data[4][1] + p6 * data[5][1] + p7 * data[6][1],
            p2)
        f3 = Eq(
            p1 * data[0][2] + p2 * data[1][2] + p3 * (data[2][2]) + p4 * data[3][2] + p5 * data[4][2] + p6 * data[5][2] + p7 * data[6][2],
            p3)
        f4 = Eq(
            p1 * data[0][3] + p2 * data[1][3] + p3 * data[2][3] + p4 * (data[3][3]) + p5 * data[4][3] + p6 * data[5][3] + p7 * data[6][3],
            p4)
        f5 = Eq(
            p1 * data[0][4] + p2 * data[1][4] + p3 * data[2][4] + p4 * data[3][4] + p5 * (data[4][4]) + p6 * data[5][4] + p7 * data[6][4],
            p5)
        f6 = Eq(
            p1 * data[0][5] + p2 * data[1][5] + p3 * data[2][5] + p4 * data[3][5] + p5 * data[4][5] + p6 * (data[5][5]) + p7 * data[6][5],
            p6)
        f7 = Eq(
            p1 * data[0][5] + p2 * data[1][5] + p3 * data[2][5] + p4 * data[3][5] + p5 * data[4][5] + p6 * (data[5][5]) + p7 * data[6][6],
            p6)
        f8 = Eq(p1 + p2 + p3 + p4 + p5 + p6 + p7, 1)
        solutions = solve((f1, f2, f3, f4, f5, f7, f8), (p1, p2, p3, p4, p5, p6 ,p7))
        print(solutions)

def cal_four_markov(data):
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



def get_loss_BD(data,rtt):
    res = []
    p1=data[6][0]*(1-data[0][0])+data[6][1]*(data[1][2]+data[1][3]+data[1][4]+data[1][5])+data[6][2]*(data[2][3]+data[2][4]+data[2][5])+data[6][3]*(data[3][4]+data[3][5])+data[6][4]*data[4][5]+data[6][5]*data[5][5]
    p2=data[6][0]*data[0][1]*(data[1][2]+data[2][3]+data[3][4]+data[4][5])+data[6][0]*data[0][2]*(data[2][3]+data[2][4]+data[2][5])+data[6][0]*data[0][3]*(data[3][4]+data[3][5])+data[6][0]*data[0][4]*data[4][5]+data[6][0]*data[0][5]*data[5][5]+data[6][1]*data[1][2]*(data[2][3]+data[2][4]+data[2][5])
    p3=0.1*p2
    p4=0.08*p3
    res.append(p1)
    res.append(p2)
    res.append(p3)
    res.append(p4)
    res.append(p4*0.1)
    x = []
    y = []
    m = []
    n = []
    x.append(0)
    y.append(0)
    m.append(0)
    n.append(0)
    temp=1-p1
    ans=temp
    t=1
    for j in range (1,800):
        if(j>600):
            temp=1
            ans=1
        elif(j%rtt==0):
            if t>=len(res):
                temp=1
            else:
                temp=1-res[t]
            t=t+1
            if temp>=ans:
                ans=temp
            else:
                if (ans * 1.03 < 1):
                    ans=ans*1.03
                else:
                    ans=1
        x.append(j)
        y.append(temp)
        if len(m)>1:
            if m[len(m)-1]>j:
                continue
        m.append(j)
        n.append(ans)
    last=n[0]
    for j in range (1,800):
        if(n[j]<n[j-1]):
            n[j]=n[j-1]






