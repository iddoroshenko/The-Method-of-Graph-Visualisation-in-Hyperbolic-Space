import random
import numpy as np
from operator import itemgetter
import subprocess, signal
from os import kill,system
import time
import math
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
#import seaborn as sns

from final_src.file_Reader import *
from final_src.ACD_main import *
def readWalrusFile(stream):
    file = open(stream, 'r')
    lines = file.readlines()
    coord = []
    for line in lines:
        i = line.split(' ')[0]
        x = line.split(' ')[1]
        y = line.split(' ')[2]
        z = line.split(' ')[3]
        coord.append((i,x,y,z))
    return coord

def readWalrus(source):
    coord = readWalrusFile(source)
    N = 0
    for node in coord:
        N = max(int(node[0]), N)
    N = N + 1
    result = []
    for i in range(N):
        result.append((0.0,0.0,0.0))
    for i in range(len(coord)):
        result[int(coord[i][0])] = (float(coord[i][1]) * 1000, float(coord[i][2]) * 1000, float(coord[i][3]) * 1000)
    return result

def area(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def intersect_1(a, b, c, d):
    if a > b:
        a,b = b,a
    if c > d:
        c,d = d,c
    return max(a,c) <= min(b,d)

def intersect(a, b, c, d):
    return intersect_1 (a[0], b[0], c[0], d[0]) \
    and intersect_1 (a[1], b[1], c[1], d[1]) \
    and area(a,b,c) * area(a,b,d) <= 0 \
    and area(c,d,a) * area(c,d,b) <= 0

def getNumOfIntersections(coord, stream_GML):    
    edges = listOfEdges(readGraph_gml(stream_GML))
    numOfIntersections = 0
    m = len(edges)
    for i in range(m):
        for j in range(i+1, m):
            a = edges[i][0]
            b = edges[i][1]
            c = edges[j][0]
            d = edges[j][1]
            a = coord[a]
            b = coord[b]
            c = coord[c]
            d = coord[d]
            #print(intersect(a, b, c, d), edges[i][0], edges[i][1], edges[j][0], edges[j][1])
            if intersect(a, b, c, d) == True and not edges[i][0] == edges[j][0] and not edges[i][0] == edges[j][1] \
            and not edges[i][1] == edges[j][0] and not edges[i][1] == edges[j][1]:
                numOfIntersections+=1
    return numOfIntersections

def rotateByX(coord, alpha):
    coordRotated = []
    for node in coord:
        x = node[0]
        y = node[1]
        z = node[2]
        newX = x
        newY = y * math.cos(alpha) + z * math.sin(alpha)
        newZ = -y * math.sin(alpha) + z * math.cos(alpha)
        coordRotated.append((newX, newY, newZ))
    return coordRotated

def rotateByY(coord, alpha):
    coordRotated = []
    for node in coord:
        x = node[0]
        y = node[1]
        z = node[2]
        newX = x * math.cos(alpha) + z * math.sin(alpha)
        newY = y
        newZ = -x * math.sin(alpha) + z * math.cos(alpha)
        coordRotated.append((newX, newY, newZ))
    return coordRotated

from ipywidgets import widgets
from IPython.display import display, clear_output

def allIntersections360(stream_TXT, stream_GML, graphNum):
    coord = readWalrus(stream_TXT)
    degree = math.pi / 180
    Intersections = []
    for i in range(180):
        clear_output()
        alphaY = i * degree
        print('#graph = ' + str(graphNum+1), flush = True)
        print(' alphaY = ' + str(i), flush = True)
        print(' Done: ' + str("%.2f" % (i/180*100)) + '%', flush = True)
        coordRotatedByY = rotateByY(coord, alphaY)
        for j in range(180):
            #clear_output()
            alphaX = j * degree
            coordRotatedByX = rotateByX(coordRotatedByY, alphaX)
            numOfIntersections = getNumOfIntersections(coordRotatedByX, stream_GML)
            Intersections.append(numOfIntersections)
    return Intersections

def getStatistic360(stream_TXT, stream_GML, gn):
    Intersections = allIntersections360(stream_TXT, stream_GML, gn)
    return str(np.array(Intersections).min())

def startRandomAndCounting(gmlFile, graphFile, randomWeight = True, times = 1, num = 0):
    ans = []
    for i in range(times):
        toWalrusSpace(gmlFile, graphFile, randomWeight)
        system('del .\\bin\\nodes.txt')
        proc = subprocess.Popen('java H3Main ' + graphFile + ' .\\bin\\nodes.txt')
        pid = proc.pid
        time.sleep(10)
        kill(pid, signal.SIGINT)
        #clear_output()
        #print('#graph = ' + str(num+1), flush = True)
        t = getStatistic360('.\\bin\\nodes.txt', gmlFile, num)
        ans.append(t)
    return ans

def addRecord(intersec, GraphName, path = '.\\bin\\stat.txt'):
    stat = open(path, 'a')
    print(str(intersec) + '\t' + GraphName, file = stat)
    stat.close()
