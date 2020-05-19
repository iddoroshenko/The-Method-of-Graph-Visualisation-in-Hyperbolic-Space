import numpy as np
def readGraph_gml(stream):    
    file = open(stream, 'r')
    lines = file.readlines()
    N = 0
    for line in lines:
        if "node" in line:
            N += 1      
    graph = np.zeros((N, N))  
    for i in range(len(lines)):
        if "source" in lines[i]:
            a = int(lines[i].split(' ')[5])        
            b = int(lines[i+1].split(' ')[5])
            i += 1
            graph[a-1][b-1] = 1
            graph[b-1][a-1] = 1
    file.close()        
    return graph #Adjacency matrix

def readGraphLabels_gml(stream):
    file = open(stream, 'r')
    lines = file.readlines()
    labels = []
    for line in lines:
        if 'label' in line:
            labels.append(line.split('\"')[1])
        if 'edge' in line:
            break
    file.close()
    return labels # labels if you need
