import subprocess, signal
from os import kill,system

def callWalrus(path):
    proc = subprocess.Popen('java H3Main ' + path + ' .\\bin\\nodes.txt')