import numpy as np

from final_src.ACD import *
from final_src.ACD_helper import *
from final_src.file_Reader import *
from final_src.mst import *

def toWalrusSpace(stream_in, stream_out, randomWeight = False):
    graph = readGraph_gml(stream_in)          
    labels = readGraphLabels_gml(stream_in)
    graph_ACD = np.zeros((1, 1))
    if randomWeight == False:
        graph_ACD = AmplifiedCommuteDistance(graph)                   
    else:
        graph_ACD = randomEdgesWeight(graph)
    root = np.arange(0,len(graph),1)
    graph_ACD = correctAdjacencyMatrix(graph_ACD, graph)
    graph_MST = mst(listOfEdges(graph_ACD), root) 
    
    graphInEdges = listOfEdges(graph)
    
    graphToWalrus = listOfEdgesToAdjacencyList(graph_MST)    
    edgesTree = mstAdjacencyListToListOfEdges(graphToWalrus)
    
    edgesNotTree = otherEdges(edgesTree, graphInEdges)
    
    
    Walrusfile = open(stream_out, 'w')
    p1 = open('..\\files_for_parsing\\p1.txt', 'r')
    p2 = open('..\\files_for_parsing\\p2.txt', 'r')
    p3 = open('..\\files_for_parsing\\p3.txt', 'r')
    p4 = open('..\\files_for_parsing\\p4.txt', 'r')
    p5 = open('..\\files_for_parsing\\p5.txt', 'r')
    p6 = open('..\\files_for_parsing\\p6.txt', 'r')
    
    lines_p1 = p1.readlines()
    for line in lines_p1:
        print(line, file = Walrusfile, end = '')
        
    print(file = Walrusfile)
    print('\t@numNodes=' + str(len(edgesTree) + 1) + ';', 
          file = Walrusfile)
    print('\t@numLinks=' + str(len(edgesNotTree) + len(edgesTree)) + ';', 
          file = Walrusfile)
    
    lines_p2 = p2.readlines()
    for line in lines_p2:
        print(line, file = Walrusfile, end = '')
        
    WalrusGraph1(edgesTree, edgesNotTree, Walrusfile)
    
    lines_p3 = p3.readlines()
    for line in lines_p3:
        print(line, file = Walrusfile, end = '')
        
    WalrusGraph2(edgesTree, Walrusfile)
        
    lines_p4 = p4.readlines()
    for line in lines_p4:
        print(line, file = Walrusfile, end = '')
        
    WalrusGraph3(edgesTree, Walrusfile)
    
    lines_p5 = p5.readlines()
    for line in lines_p5:
        print(line, file = Walrusfile, end = '')
        
    WalrusGraph4(labels, Walrusfile)
    
    lines_p6 = p6.readlines()
    for line in lines_p6:
        print(line, file = Walrusfile, end = '')
        
    Walrusfile.close()
    p1.close()
    p2.close()
    p3.close()
    p4.close()
    p5.close()
    p6.close()

def toGephiSpace(stream_in, stream_out):
    graph = readGraph_gml(stream_in)
    labels = readGraphLabels_gml(stream_in)
    graph_ACD = AmplifiedCommuteDistance(graph)  
    
    root = np.arange(0,len(graph),1)
    
    graph_ACD = correctAdjacencyMatrix(graph_ACD, graph)
    graph_MST = mst(listOfEdges(graph_ACD), root) 
    
    graphInEdges = listOfEdges(graph)
   
    graphToWalrus = listOfEdgesToAdjacencyList(graph_MST)    
    edgesTree = mstAdjacencyListToListOfEdges(graphToWalrus)
    
    edgesNotTree = otherEdges(edgesTree, graphInEdges)
    GephiFile = open(stream_out, 'w')
    print('graph\n[', file = GephiFile)
    n = graph.shape[0]
    for i in range(n):
        if len(labels) > 0:
            print('  node\n  [\n\tid ' + str(i) + '\n\tlabel \"' + labels[i] + '\"\n  ]', file = GephiFile)
        else :
            print('  node\n  [\n\tid ' + str(i) + '\n  ]', file = GephiFile)
    for edge in edgesTree:
        print('  edge\n  [\n\tsource ' + str(edge[0]) + \
              '\n\ttarget ' + str(edge[1]) + '\n\tregulation \"tree\"\n  ]', file = GephiFile)
    for edge in edgesNotTree:
        print('  edge\n  [\n\tsource ' + str(edge[0]) + \
              '\n\ttarget ' + str(edge[1]) + '\n\tregulation \"Not tree\"\n  ]', file = GephiFile)