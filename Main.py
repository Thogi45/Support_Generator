import os,sys, glob
import Locate_STL
from stl import mesh, Mesh
import subprocess

LocateSTL=os.path.dirname(sys.argv[0])
print("----------------------------------------\n")
print("            SUPPORT GENERATOR              \n")
print("by Thomas Heissel and Thomas Girerd       ")
print("----------------------------------------\n")
print("You need to choose the STL file you want to generate supports with.")
STL=Locate_STL.STL

