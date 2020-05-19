import numpy as np


def correctAdjacencyMatrix(ACD, AdjacencyMatrix):
    n = ACD.shape[0]
    for i in range(n):
        for j in range(n):
            if AdjacencyMatrix[i][j] == 0:
                ACD[i][j] = 0
    return ACD

def listOfEdges(graph):
    n = graph.shape[0]
    lst = []
    for i in range(n):
        for j in range(i+1, n):
            if graph[i][j] != 0:
                lst.append((i,j,graph[i][j]))
    
    return lst

def listOfEdgesToAdjacencyList(edges):
    matrix = []
    n = len(edges) + 1
    for i in range(0,n):
        matrix.append([])
    for edge in edges:
        matrix[edge[0]].append(edge[1])
        matrix[edge[1]].append(edge[0])
    return matrix

def mstAdjacencyListToListOfEdges(toWalrus):
    toWalrusCopy = toWalrus
    was = np.zeros(len(toWalrus))
    toWalrus_Edges = []
    dfs(0, was, toWalrusCopy, toWalrus_Edges)
    return toWalrus_Edges

def dfs(x, was, toWalrusCopy, toWalrus_Edges): 
    was[x] = 1
    for y in toWalrusCopy[x]:
        if was[y] == 0:
            toWalrus_Edges.append((x, y))
            dfs(y, was, toWalrusCopy, toWalrus_Edges)
            
def WalrusGraph1(edges, edgesNotTree, outFile):
    n = len(edges)
    for i in range(n):
            print('\t\t{ @source=' + str(edges[i][0]) + '; @destination=' + str(edges[i][1]) + '; },', 
                 file = outFile) 
    n = len(edgesNotTree)
    for i in range(n):
        if not i == n - 1:
            print('\t\t{ @source=' + str(edgesNotTree[i][0]) + '; @destination=' + str(edgesNotTree[i][1]) + '; },', 
                 file = outFile) 
        else:
             print('\t\t{ @source=' + str(edgesNotTree[i][0]) + '; @destination=' + str(edgesNotTree[i][1]) + '; }', 
                 file = outFile)    

def WalrusGraph2(edges, outFile):
    n = len(edges)
    for i in range(n):
        if not i == n - 1:
            print('\t\t\t\t{ @id=' + str(i) + '; @value=T; },', file = outFile)
        else:
            print('\t\t\t\t{ @id=' + str(i) + '; @value=T; }', file = outFile)
    
def WalrusGraph3(edges, outFile):    
    n = len(edges) + 1
    for i in range(0, n):
        if not i == n - 1:
            print('\t\t\t\t{ @id=' + str(i) +'; @value=' + str(i+1) + '; },', file = outFile)
        else:
            print('\t\t\t\t{ @id=' + str(i) +'; @value=' + str(i+1) + '; }', file = outFile)
            
def WalrusGraph4(labels, outFile):    
    n = len(labels)
    for i in range(0, n):
        if not i == n - 1:
            print('\t\t\t\t{ @id=' + str(i) +'; @value=\"' + labels[i] + '\"; },', file = outFile)
        else:
            print('\t\t\t\t{ @id=' + str(i) +'; @value=\"' + labels[i] + '\"; }', file = outFile)

def otherEdges(tree, allEdges):
    edgesNotTree = []
    for edge in allEdges:
        if not (min(edge[0], edge[1]), max(edge[0], edge[1])) in tree and \
           not (max(edge[0], edge[1]), min(edge[0], edge[1])) in tree:
            edgesNotTree.append((min(edge[0], edge[1]), max(edge[0], edge[1])))
    return edgesNotTree

