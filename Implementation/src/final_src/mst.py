from operator import itemgetter

def get(x, root):
    if root[x] == x:
        return x
    root[x] = get(root[x], root)
    return root[x]

def merge(a, b, root):
    a = get(a, root)
    b = get(b, root)
    root[a] = b

def mst(edges, root):
    edges = sorted(edges, key=itemgetter(2))
    treeEdges = []
    for edge in edges:
        x = edge[0]
        y = edge[1]
        if get(x, root) != get(y, root):
            merge(x, y, root)
            treeEdges.append((edge[0], edge[1]))
    return treeEdges