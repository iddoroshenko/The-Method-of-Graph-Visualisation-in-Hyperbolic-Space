import numpy as np
def AmplifiedCommuteDistance(graph):
    n = graph.shape[0]
    volG = 0
    D = np.zeros((n, n))
    for i in range(0,n):
        degree = 0
        for j in range(0,n):
            degree += graph[i][j]
            volG += graph[i][j]
        D[i][i] = degree
    A = graph.copy()
    L = D - A
    L = np.linalg.pinv(L)
    d = np.zeros((n, n))
    for i in range(0,n):
        d[i][i]  = 0
        ei = np.zeros((1,n))
        ei[0][i] = 1
        for j in range(i+1,n):
            ej = np.zeros((1,n))
            ej[0][j] = 1
            
            left = ei - ej
            
            left = left.dot(L)
            
            right = ei.transpose() - ej.transpose()
            
            left = left.dot(right)
            
            R_ij = left[0][0]            
            d_i = D[i][i]
            d_j = D[j][j]
            S_ij = R_ij - 1/d_i - 1/d_j
            u_ij = 2 * graph[i][j] / (d_i*d_j) - graph[i][i] / (d_i*d_i) - graph[j][j] / (d_j*d_j)
            if S_ij + u_ij < 0:
                Camp_ij = 0
            else:
                Camp_ij = np.sqrt( S_ij + u_ij )
            
            d[i][j] = Camp_ij
            d[j][i] = Camp_ij
    return d

import random
def randomEdgesWeight(graph):
    n = graph.shape[0]
    D = np.zeros((n, n))
    for i in range(0,n):
        for j in range(0,n):
            D[i][j] = random.randint(1,100)
    return D